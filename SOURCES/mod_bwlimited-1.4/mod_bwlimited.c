#include "httpd.h"
#include "http_core.h"
#include "http_config.h"
#include "http_log.h"
#include "http_request.h"
#include "apr_strings.h"
#include "mod_core.h"
#include "http_protocol.h"
#include "unistd.h"

#define BWROOT "/var/cpanel/bwlimited"
#define BWLIMITHTML "/usr/local/cpanel/etc/bwlimit.html"
#define HTTP_BANDWIDTH_LIMIT_EXCEEDED 509

extern module AP_MODULE_DECLARE_DATA bwlimited_module;

static int check_bwlimit (request_rec * r)
{
  char *filename;
  char *name = r->uri;
  char str[HUGE_STRING_LEN];
  const char *w, *dname;
  apr_bucket_brigade *bb = apr_brigade_create(r->pool, r->connection->bucket_alloc);

  if ((name[0] != '/') || (name[1] != '~'))
    {
      if (r->server->server_hostname == NULL)
	{
	  return DECLINED;
	}
      strncpy (str, r->server->server_hostname, (HUGE_STRING_LEN - 1));
      filename = apr_pstrcat (r->pool, BWROOT, "/", str, NULL);
    }
  else
    {
      dname = name + 2;
      w = ap_getword (r->pool, &dname, '/');
      if (dname[-1] == '/')
	{
	  --dname;
	}
      if (w[0] == '\0'
	  || (w[1] == '.' && (w[2] == '\0' || (w[2] == '.' && w[3] == '\0'))))
	{
	  return DECLINED;
	}

      filename = apr_pstrcat (r->pool, BWROOT, "/", w, NULL);
    }
  if (!access (filename, F_OK))
    {
      int i;
      r->status = HTTP_INTERNAL_SERVER_ERROR;
      r->content_type = "text/html";
      ap_basic_http_header (r, bb); /* , apr_bucket_brigade * bb); */
      ap_rvputs (r,
		 "\n"
		 DOCTYPE_HTML_2_0
		 "<HTML><HEAD>\n<TITLE>509 Bandwidth Limit Exceeded</TITLE>\n"
		 "</HEAD><BODY>\n"
		 "<H1>Bandwidth Limit Exceeded</H1>\n", NULL);
      for (i = 0; i < 1000; i++)
	{
	  ap_rvputs (r, "      \n", NULL);
	}
      ap_rputs ("The server is temporarily unable to service your\n"
		"request due to the site owner reaching his/her\n"
		"bandwidth limit. Please try again later.\n", r);
      ap_rputs (ap_psignature ("<HR>\n", r), r);
      ap_rputs ("</BODY></HTML>\n", r);
      /* ap_kill_timeout (r); */
      ap_finalize_request_protocol (r);
      ap_rflush (r);
      return DONE;
    }
  return DECLINED;
}

  /* this worked instead of (void) */
  /* static void bwlimited_version(server_rec * s, apr_pool_t * p) */
static int bwlimited_version (apr_pool_t * p, apr_pool_t * pLog, apr_pool_t * pTemp, server_rec * s)
{
  ap_add_version_component (p, "mod_bwlimited/1.4");
  return OK;
}

static void register_hooks(apr_pool_t * p)
{
  /* warning: passing arg 1 of `ap_hook_post_config' from incompatible pointer type */
  ap_hook_post_config(bwlimited_version,NULL,NULL,APR_HOOK_MIDDLE);
  ap_hook_fixups(check_bwlimit,NULL,NULL,APR_HOOK_MIDDLE);
};

module AP_MODULE_DECLARE_DATA bwlimited_module =
{
  STANDARD20_MODULE_STUFF,
  NULL,           /* create per-directory config structures */
  NULL,           /* merge per-directory config structures  */
  NULL,           /* create per-server config structures    */
  NULL,           /* merge per-server config structures     */
  NULL,           /* command table */
  register_hooks  /* register hooks */
};
