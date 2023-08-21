# Copyright 2023 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python function-based components used in KFP pipelies."""
import functools
from typing import List, NamedTuple, Optional

from google_cloud_pipeline_components import _image
from google_cloud_pipeline_components._implementation.llm import env
from kfp import dsl


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_machine_spec(
    location: str,
    use_test_spec: bool = False,
) -> NamedTuple(
    'MachineSpec', machine_type=str, accelerator_type=str, accelerator_count=int
):
  """Returns machine spec to use for a given location.

  Args:
    location: Where the machine will run.
    use_test_spec: Whether to use a lower resource machine for testing.

  Returns:
    Machine spec.

  Raises:
    ValueError: If accelerators are requested in an unsupported location.
  """
  outputs = NamedTuple(
      'MachineSpec',
      machine_type=str,
      accelerator_type=str,
      accelerator_count=int,
  )
  tpu_regions = {'europe-west4'}
  gpu_regions = {'us-central1'}
  if use_test_spec:
    return outputs(
        machine_type='a2-highgpu-1g',
        accelerator_type='NVIDIA_TESLA_A100',
        accelerator_count=1,
    )
  elif location in tpu_regions:
    return outputs(
        machine_type='cloud-tpu',
        accelerator_type='TPU_V3',
        accelerator_count=32,
    )
  elif location in gpu_regions:
    return outputs(
        machine_type='a2-ultragpu-8g',
        accelerator_type='NVIDIA_A100_80GB',
        accelerator_count=8,
    )
  raise ValueError(
      f'Unsupported accelerator location {location}. Must be one of'
      f' {tpu_regions | gpu_regions}.'
  )


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_image_uri(
    image_name: str,
    project: str,
    location: str,
    artifact_registry: str,
    image_name_prefix: str,
    tag: str,
    accelerator_type: str = '',
    accelerator_count: int = 0,
) -> str:
  """Generates image uri based on base image name and accelerator type.

  Args:
    image_name: Base image name, e.g. ``'sft'`` or ``'reward_model'``.
    project: Project that contains the artifact registry.
    location: Region that contains the artifact registry.
    artifact_registry: Registry that contains Docker images.
    image_name_prefix: Text to prepend to the base image name.
    tag: Image tag.
    accelerator_type: One of the supported accelerator types, e.g. ``'TPU_V3'``.
    accelerator_count: Number of accelerators.

  Returns:
    Docker image uri

  Raises:
    ValueError: if an unsupported accelerator type is provided.
  """
  cpu_only_images = {
      'text_importer',
      'text_comparison_importer',
  }

  if image_name in cpu_only_images:
    accelerator_postfix = ''
  elif accelerator_type == 'TPU_V3':
    accelerator_postfix = '_tpu'
  elif accelerator_type == 'NVIDIA_A100_80GB' and accelerator_count == 8:
    accelerator_postfix = '_gpu_test'
  else:
    accelerator_postfix = '_gpu'

  backup_images = {
      'sft',
      'reward_model',
      'reinforcer',
      'infer',
      'text_importer',
      'text_comparison_importer',
  }
  if image_name in backup_images and accelerator_postfix != '_gpu_test':
    accelerator_postfix += '_backup'
  return f'{location}-docker.pkg.dev/{project}/{artifact_registry}/{image_name_prefix}{image_name}{accelerator_postfix}:{tag}'


# Resolves image uri from the environment's private artifact registry.
# By default this resolves an image in the vertex private registry.
resolve_private_image_uri = functools.partial(
    resolve_image_uri,
    project=env.PRIVATE_ARTIFACT_REGISTRY_PROJECT,
    location=env.PRIVATE_ARTIFACT_REGISTRY_LOCATION,
    artifact_registry=env.PRIVATE_ARTIFACT_REGISTRY,
    image_name_prefix=env.PRIVATE_IMAGE_NAME_PREFIX,
    tag=env.get_private_image_tag(),
)


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_data_paths(
    input_dataset: str,
) -> NamedTuple('DataPaths', tfds_data_dir=str, tfds_name=str):
  """Resolves dataset paths needed by downstream components."""
  # pylint: disable=g-import-not-at-top,import-outside-toplevel,redefined-outer-name,reimported
  import os
  # pylint: enable=g-import-not-at-top,import-outside-toplevel,redefined-outer-name,reimported
  outputs = NamedTuple('DataPaths', tfds_data_dir=str, tfds_name=str)
  tfds_data_dir, tfds_name = os.path.split(input_dataset)
  return outputs(
      tfds_data_dir=tfds_data_dir,
      tfds_name=tfds_name,
  )


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_reference_model_metadata(
    large_model_reference: str,
    reference_model_path: Optional[str] = None,
) -> NamedTuple(
    'BaseModelMetadata',
    large_model_reference=str,
    reference_model_path=str,
    reward_model_reference=str,
    reward_model_path=str,
):
  """Resolves reference model metadata needed by downstream components.

  Args:
    large_model_reference: User-provided reference model name.
    reference_model_path: Optional path to a tuned based model to use in place
      of the default base model. If specified, the model at this path must be a
      tuned version of the base model associated with ``large_model_reference``.

  Returns:
    Base model name (used by downstream components to find gin configs and load
    vocabularies) and the path to the base model checkpoint.

  Raises:
    ValueError: if no metadata exists for the given base model.
  """

  # TODO(latture): Move this logic to a container component and use
  #                PredefinedModels enum to resolve model paths.
  outputs = NamedTuple(
      'BaseModelMetadata',
      large_model_reference=str,
      reference_model_path=str,
      reward_model_reference=str,
      reward_model_path=str,
  )
  reference_model_key = large_model_reference.upper().replace('-', '_')
  predefined_model_paths = {
      'PALM_TINY': (
          'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_palm_tiny/'
      ),
      'GECKO': 'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_gecko/',
      'OTTER': 'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_otter/',
      'BISON': 'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_bison/',
      'ELEPHANT': (
          'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_elephant/'
      ),
      'T5_SMALL': 'gs://t5-data/pretrained_models/t5x/flan_t5_small/',
      'T5_LARGE': 'gs://t5-data/pretrained_models/t5x/flan_t5_large/',
      'T5_XL': 'gs://t5-data/pretrained_models/t5x/flan_t5_xl/',
      'T5_XXL': 'gs://t5-data/pretrained_models/t5x/flan_t5_xxl/',
  }
  predefined_reward_model_paths = {
      'PALM_TINY': (
          'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_palm_tiny'
      ),
      'GECKO': 'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_gecko_pretrain',
      'OTTER': 'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_otter_pretrain',
      'ELEPHANT': (
          'gs://vertex-rlhf-restricted/pretrained_models/palm/t5x_elephant/'
      ),
      'T5_SMALL': 'gs://t5-data/pretrained_models/t5x/t5_1_1_small',
      'T5_LARGE': 'gs://t5-data/pretrained_models/t5x/t5_1_1_large',
      'T5_XL': 'gs://t5-data/pretrained_models/t5x/t5_1_1_xl',
      'T5_XXL': 'gs://t5-data/pretrained_models/t5x/t5_1_1_xxl',
  }

  if reference_model_key not in predefined_model_paths:
    raise ValueError(
        f'No metadata found for `{reference_model_key}`. '
        f'Base model must be one of {list(predefined_model_paths.keys())}.'
    )

  # Mapping from base model to its corresponding reward model.
  reference_model_to_reward_model = {
      'PALM_TINY': 'PALM_TINY',
      'GECKO': 'GECKO',
      'OTTER': 'OTTER',
      'BISON': 'OTTER',
      'ELEPHANT': 'ELEPHANT',
      'T5_SMALL': 'T5_SMALL',
      'T5_LARGE': 'T5_LARGE',
      'T5_XL': 'T5_XL',
      'T5_XXL': 'T5_XXL',
  }

  reward_model_key = reference_model_to_reward_model[reference_model_key]

  return outputs(
      large_model_reference=reference_model_key,
      reference_model_path=(
          reference_model_path or predefined_model_paths[reference_model_key]
      ),
      reward_model_reference=reward_model_key,
      reward_model_path=predefined_reward_model_paths[reward_model_key],
  )


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def convert_to_delimited_string(items: List[str], delimiter: str = ',') -> str:
  """Converts a list of strings to single string delimited by the specified character."""
  return delimiter.join(items)


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def generate_default_instruction(
    task: str,
    target_sequence_length: int,
    instruction_override: str = '',
) -> str:
  """Generates a default instruction if no override is provided."""
  if instruction_override:
    return instruction_override
  task = task.lower()
  if task == 'summarization':
    return f'Summarize in less than {target_sequence_length} words.'
  else:
    raise ValueError(
        f'Task not recognized: {task}. Supported tasks are: summarization.'
    )


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_upload_location(upload_location: Optional[str] = None) -> str:
  """Gets the region to upload the model.

  Args:
    upload_location: User-specified region to upload the model to.

  Returns:
    Where to upload the model. If no location is specified, the model will be
    uploaded to the region where the pipeline is running.
  """
  # pylint: disable=g-import-not-at-top
  import os
  # pylint: enable=g-import-not-at-top
  return upload_location or os.environ['CLOUD_ML_REGION']


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_regional_endpoint(upload_location: str) -> str:
  """Gets the regional endpoint used to upload a model to the registry.

  Args:
    upload_location: Region where the model will be uploaded.

  Returns:
    Regional endpoint.
  """
  return f'https://{upload_location}-aiplatform.googleapis.com/ui'


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_model_display_name(
    large_model_reference: str,
    model_display_name: Optional[str] = None,
) -> str:
  """Gets the model display name shown in the registry and used for endpoints.

  Args:
    large_model_reference: Base model tuned by the pipeline.
    model_display_name: User-provided display name. If not provided, a default
      display name will be created.

  Returns:
    Either the user-provided name or a default display name with the form
    ``{large_model_reference}-{timestamp}``
  """
  # pylint: disable=g-import-not-at-top
  import datetime
  # pylint: enable=g-import-not-at-top
  now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  return model_display_name or f'{large_model_reference.lower()}-{now}'


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_deploy_model(
    deploy_model: bool, large_model_reference: str
) -> bool:
  """Resolves runtime parameter that determines whether the tuned model should be deployed."""
  supported_models = {'BISON'}
  if deploy_model and large_model_reference in supported_models:
    return True
  return False


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def value_exists(value: Optional[str] = None) -> bool:
  """Returns whether a runtime parameter was provided.

  Args:
    value: That might have been provided.

  Returns:
    Whether the string is not None and non-empty.
  """
  if not value:
    return False
  return True


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_candidate_columns(
    candidate_columns: Optional[List[str]] = None,
) -> List[str]:
  """Returns candidate columns provided by the user or the default: ['candidate_0', 'candidate_1']."""
  return candidate_columns or ['candidate_0', 'candidate_1']


@dsl.component(base_image=_image.GCPC_IMAGE_TAG, install_kfp_package=False)
def resolve_upload_model(large_model_reference: str) -> bool:
  """Returns whether the model should be uploaded."""
  supported_models = {'BISON'}
  if large_model_reference in supported_models:
    return True
  return False