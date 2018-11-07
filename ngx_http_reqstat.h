#include <nginx.h>
#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>


typedef struct ngx_http_reqstat_rbnode_s ngx_http_reqstat_rbnode_t;

typedef ngx_int_t (*ngx_http_input_body_filter_pt)
    (ngx_http_request_t *r, ngx_buf_t *buf);

extern ngx_http_input_body_filter_pt     ngx_http_top_input_body_filter;


struct ngx_http_reqstat_rbnode_s {
    u_char                       color;
    u_char                       padding[3];
    uint32_t                     len;
    ngx_queue_t                  queue;
    ngx_atomic_t                 bytes_in;
    ngx_atomic_t                 bytes_out;
    ngx_atomic_t                 conn_total;
    ngx_atomic_t                 req_total;
    ngx_atomic_t                 http_2xx;
    ngx_atomic_t                 http_3xx;
    ngx_atomic_t                 http_4xx;
    ngx_atomic_t                 http_5xx;
    ngx_atomic_t                 other_status;
    ngx_atomic_t                 rt;
    ngx_atomic_t                 ureq;
    ngx_atomic_t                 urt;
    ngx_atomic_t                 utries;
    ngx_atomic_t                 http_403;
    ngx_atomic_t                 http_404;
    ngx_atomic_t                 http_499;
    ngx_atomic_t                 http_500;
    ngx_atomic_t                 http_502;
    ngx_atomic_t                 http_504;
    ngx_atomic_t                 ups_5xx;
    ngx_atomic_t                 ups_4xx;
    ngx_atomic_t                 ups_502;
    ngx_atomic_t                 ups_504;
    u_char                       data[1];
};


typedef struct {
    ngx_array_t                 *monitor;
    ngx_array_t                 *display;
    ngx_array_t                 *bypass;
} ngx_http_reqstat_conf_t;


typedef struct {
    ngx_rbtree_t                 rbtree;
    ngx_rbtree_node_t            sentinel;
    ngx_queue_t                  queue;
} ngx_http_reqstat_shctx_t;


typedef struct {
    ngx_str_t                   *val;
    ngx_slab_pool_t             *shpool;
    ngx_http_reqstat_shctx_t    *sh;
    ngx_http_complex_value_t     value;
} ngx_http_reqstat_ctx_t;


#define NGX_HTTP_REQSTAT_BYTES_IN                                       \
    offsetof(ngx_http_reqstat_rbnode_t, bytes_in)

#define NGX_HTTP_REQSTAT_BYTES_OUT                                      \
    offsetof(ngx_http_reqstat_rbnode_t, bytes_out)

#define NGX_HTTP_REQSTAT_CONN_TOTAL                                     \
    offsetof(ngx_http_reqstat_rbnode_t, conn_total)

#define NGX_HTTP_REQSTAT_REQ_TOTAL                                      \
    offsetof(ngx_http_reqstat_rbnode_t, req_total)

#define NGX_HTTP_REQSTAT_2XX                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_2xx)

#define NGX_HTTP_REQSTAT_3XX                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_3xx)

#define NGX_HTTP_REQSTAT_4XX                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_4xx)

#define NGX_HTTP_REQSTAT_5XX                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_5xx)

#define NGX_HTTP_REQSTAT_OTHER_STATUS                                   \
    offsetof(ngx_http_reqstat_rbnode_t, other_status)

#define NGX_HTTP_REQSTAT_RT                                             \
    offsetof(ngx_http_reqstat_rbnode_t, rt)

#define NGX_HTTP_REQSTAT_UPS_REQ                                        \
    offsetof(ngx_http_reqstat_rbnode_t, ureq)

#define NGX_HTTP_REQSTAT_UPS_RT                                         \
    offsetof(ngx_http_reqstat_rbnode_t, urt)

#define NGX_HTTP_REQSTAT_UPS_TRIES                                      \
    offsetof(ngx_http_reqstat_rbnode_t, utries)

#define NGX_HTTP_REQSTAT_403                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_403)

#define NGX_HTTP_REQSTAT_404                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_404)

#define NGX_HTTP_REQSTAT_499                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_499)

#define NGX_HTTP_REQSTAT_500                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_500)

#define NGX_HTTP_REQSTAT_502                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_502)

#define NGX_HTTP_REQSTAT_504                                            \
    offsetof(ngx_http_reqstat_rbnode_t, http_504)

#define NGX_HTTP_REQSTAT_UPS_4XX                                        \
    offsetof(ngx_http_reqstat_rbnode_t, ups_4xx)

#define NGX_HTTP_REQSTAT_UPS_5XX                                        \
    offsetof(ngx_http_reqstat_rbnode_t, ups_5xx)

#define NGX_HTTP_REQSTAT_UPS_502                                        \
    offsetof(ngx_http_reqstat_rbnode_t, ups_502)

#define NGX_HTTP_REQSTAT_UPS_504                                        \
    offsetof(ngx_http_reqstat_rbnode_t, ups_504)

#define REQ_FIELD(node, offset)                                         \
    ((ngx_atomic_t *) ((char *) node + offset))
