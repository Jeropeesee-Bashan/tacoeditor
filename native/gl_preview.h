#ifndef TACO_EDITOR_GL_PREVIEW_H_
#define TACO_EDITOR_GL_PREVIEW_H_

#include <gtk/gtk.h>

G_BEGIN_DECLS

#define TACO_EDITOR_GL_PREVIEW_TYPE taco_editor_gl_preview_get_type()
G_DECLARE_FINAL_TYPE(TacoEditorGLPreview,
                     taco_editor_gl_preview,
                     TACO_EDITOR,
                     GL_PREVIEW,
                     GtkGLArea)

/**
* taco_editor_gl_preview_new:
*
* Creates a new #TacoEditorGLPreview widget.
*
* Returns: (transfer full): A new #TacoEditorGLPreview widget.
*/
GtkWidget *
taco_editor_gl_preview_new(void);

G_END_DECLS

#endif /* TACO_EDITOR_GL_PREVIEW_H_ */
