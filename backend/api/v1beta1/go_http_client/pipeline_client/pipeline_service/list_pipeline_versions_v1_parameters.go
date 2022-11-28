// Code generated by go-swagger; DO NOT EDIT.

package pipeline_service

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"context"
	"net/http"
	"time"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/runtime"
	cr "github.com/go-openapi/runtime/client"
	"github.com/go-openapi/swag"

	strfmt "github.com/go-openapi/strfmt"
)

// NewListPipelineVersionsV1Params creates a new ListPipelineVersionsV1Params object
// with the default values initialized.
func NewListPipelineVersionsV1Params() *ListPipelineVersionsV1Params {
	var (
		resourceKeyTypeDefault = string("UNKNOWN_RESOURCE_TYPE")
	)
	return &ListPipelineVersionsV1Params{
		ResourceKeyType: &resourceKeyTypeDefault,

		timeout: cr.DefaultTimeout,
	}
}

// NewListPipelineVersionsV1ParamsWithTimeout creates a new ListPipelineVersionsV1Params object
// with the default values initialized, and the ability to set a timeout on a request
func NewListPipelineVersionsV1ParamsWithTimeout(timeout time.Duration) *ListPipelineVersionsV1Params {
	var (
		resourceKeyTypeDefault = string("UNKNOWN_RESOURCE_TYPE")
	)
	return &ListPipelineVersionsV1Params{
		ResourceKeyType: &resourceKeyTypeDefault,

		timeout: timeout,
	}
}

// NewListPipelineVersionsV1ParamsWithContext creates a new ListPipelineVersionsV1Params object
// with the default values initialized, and the ability to set a context for a request
func NewListPipelineVersionsV1ParamsWithContext(ctx context.Context) *ListPipelineVersionsV1Params {
	var (
		resourceKeyTypeDefault = string("UNKNOWN_RESOURCE_TYPE")
	)
	return &ListPipelineVersionsV1Params{
		ResourceKeyType: &resourceKeyTypeDefault,

		Context: ctx,
	}
}

// NewListPipelineVersionsV1ParamsWithHTTPClient creates a new ListPipelineVersionsV1Params object
// with the default values initialized, and the ability to set a custom HTTPClient for a request
func NewListPipelineVersionsV1ParamsWithHTTPClient(client *http.Client) *ListPipelineVersionsV1Params {
	var (
		resourceKeyTypeDefault = string("UNKNOWN_RESOURCE_TYPE")
	)
	return &ListPipelineVersionsV1Params{
		ResourceKeyType: &resourceKeyTypeDefault,
		HTTPClient:      client,
	}
}

/*ListPipelineVersionsV1Params contains all the parameters to send to the API endpoint
for the list pipeline versions v1 operation typically these are written to a http.Request
*/
type ListPipelineVersionsV1Params struct {

	/*Filter
	  A base-64 encoded, JSON-serialized Filter protocol buffer (see
	filter.proto).

	*/
	Filter *string
	/*PageSize
	  The number of pipeline versions to be listed per page. If there are more
	pipeline versions than this number, the response message will contain a
	nextPageToken field you can use to fetch the next page.

	*/
	PageSize *int32
	/*PageToken
	  A page token to request the next page of results. The token is acquried
	from the nextPageToken field of the response from the previous
	ListPipelineVersions call or can be omitted when fetching the first page.

	*/
	PageToken *string
	/*ResourceKeyID
	  The ID of the resource that referred to.

	*/
	ResourceKeyID *string
	/*ResourceKeyType
	  The type of the resource that referred to.

	*/
	ResourceKeyType *string
	/*SortBy
	  Can be format of "field_name", "field_name asc" or "field_name desc"
	Ascending by default.

	*/
	SortBy *string

	timeout    time.Duration
	Context    context.Context
	HTTPClient *http.Client
}

// WithTimeout adds the timeout to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithTimeout(timeout time.Duration) *ListPipelineVersionsV1Params {
	o.SetTimeout(timeout)
	return o
}

// SetTimeout adds the timeout to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetTimeout(timeout time.Duration) {
	o.timeout = timeout
}

// WithContext adds the context to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithContext(ctx context.Context) *ListPipelineVersionsV1Params {
	o.SetContext(ctx)
	return o
}

// SetContext adds the context to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetContext(ctx context.Context) {
	o.Context = ctx
}

// WithHTTPClient adds the HTTPClient to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithHTTPClient(client *http.Client) *ListPipelineVersionsV1Params {
	o.SetHTTPClient(client)
	return o
}

// SetHTTPClient adds the HTTPClient to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetHTTPClient(client *http.Client) {
	o.HTTPClient = client
}

// WithFilter adds the filter to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithFilter(filter *string) *ListPipelineVersionsV1Params {
	o.SetFilter(filter)
	return o
}

// SetFilter adds the filter to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetFilter(filter *string) {
	o.Filter = filter
}

// WithPageSize adds the pageSize to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithPageSize(pageSize *int32) *ListPipelineVersionsV1Params {
	o.SetPageSize(pageSize)
	return o
}

// SetPageSize adds the pageSize to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetPageSize(pageSize *int32) {
	o.PageSize = pageSize
}

// WithPageToken adds the pageToken to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithPageToken(pageToken *string) *ListPipelineVersionsV1Params {
	o.SetPageToken(pageToken)
	return o
}

// SetPageToken adds the pageToken to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetPageToken(pageToken *string) {
	o.PageToken = pageToken
}

// WithResourceKeyID adds the resourceKeyID to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithResourceKeyID(resourceKeyID *string) *ListPipelineVersionsV1Params {
	o.SetResourceKeyID(resourceKeyID)
	return o
}

// SetResourceKeyID adds the resourceKeyId to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetResourceKeyID(resourceKeyID *string) {
	o.ResourceKeyID = resourceKeyID
}

// WithResourceKeyType adds the resourceKeyType to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithResourceKeyType(resourceKeyType *string) *ListPipelineVersionsV1Params {
	o.SetResourceKeyType(resourceKeyType)
	return o
}

// SetResourceKeyType adds the resourceKeyType to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetResourceKeyType(resourceKeyType *string) {
	o.ResourceKeyType = resourceKeyType
}

// WithSortBy adds the sortBy to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) WithSortBy(sortBy *string) *ListPipelineVersionsV1Params {
	o.SetSortBy(sortBy)
	return o
}

// SetSortBy adds the sortBy to the list pipeline versions v1 params
func (o *ListPipelineVersionsV1Params) SetSortBy(sortBy *string) {
	o.SortBy = sortBy
}

// WriteToRequest writes these params to a swagger request
func (o *ListPipelineVersionsV1Params) WriteToRequest(r runtime.ClientRequest, reg strfmt.Registry) error {

	if err := r.SetTimeout(o.timeout); err != nil {
		return err
	}
	var res []error

	if o.Filter != nil {

		// query param filter
		var qrFilter string
		if o.Filter != nil {
			qrFilter = *o.Filter
		}
		qFilter := qrFilter
		if qFilter != "" {
			if err := r.SetQueryParam("filter", qFilter); err != nil {
				return err
			}
		}

	}

	if o.PageSize != nil {

		// query param page_size
		var qrPageSize int32
		if o.PageSize != nil {
			qrPageSize = *o.PageSize
		}
		qPageSize := swag.FormatInt32(qrPageSize)
		if qPageSize != "" {
			if err := r.SetQueryParam("page_size", qPageSize); err != nil {
				return err
			}
		}

	}

	if o.PageToken != nil {

		// query param page_token
		var qrPageToken string
		if o.PageToken != nil {
			qrPageToken = *o.PageToken
		}
		qPageToken := qrPageToken
		if qPageToken != "" {
			if err := r.SetQueryParam("page_token", qPageToken); err != nil {
				return err
			}
		}

	}

	if o.ResourceKeyID != nil {

		// query param resource_key.id
		var qrResourceKeyID string
		if o.ResourceKeyID != nil {
			qrResourceKeyID = *o.ResourceKeyID
		}
		qResourceKeyID := qrResourceKeyID
		if qResourceKeyID != "" {
			if err := r.SetQueryParam("resource_key.id", qResourceKeyID); err != nil {
				return err
			}
		}

	}

	if o.ResourceKeyType != nil {

		// query param resource_key.type
		var qrResourceKeyType string
		if o.ResourceKeyType != nil {
			qrResourceKeyType = *o.ResourceKeyType
		}
		qResourceKeyType := qrResourceKeyType
		if qResourceKeyType != "" {
			if err := r.SetQueryParam("resource_key.type", qResourceKeyType); err != nil {
				return err
			}
		}

	}

	if o.SortBy != nil {

		// query param sort_by
		var qrSortBy string
		if o.SortBy != nil {
			qrSortBy = *o.SortBy
		}
		qSortBy := qrSortBy
		if qSortBy != "" {
			if err := r.SetQueryParam("sort_by", qSortBy); err != nil {
				return err
			}
		}

	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}