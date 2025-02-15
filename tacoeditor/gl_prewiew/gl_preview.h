#ifndef TACO_GL_PREVIEW_H_
#define TACO_GL_PREVIEW_H_

#include <gtk/gtk.h>

G_BEGIN_DECLS

#define TACO_GL_PREVIEW_TYPE (taco_gl_preview_get_type())
G_DECLARE_FINAL_TYPE(TacoGLPreview, taco_gl_preview, TACO, GL_PREVIEW, GtkGLArea)

struct _TacoGLPreview {
    GtkGLArea parent_instance;
};

/**
* taco_gl_preview_new:
*
* Creates a new #TacoGLPreview widget.
*
* Returns: (transfer full): A new #TacoGLPreview widget.
*/
GtkWidget *taco_gl_preview_new(void);

G_END_DECLS

#endif /* TACO_GL_PREVIEW_H_ */
