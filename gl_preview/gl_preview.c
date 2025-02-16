#include "gl_preview.h"

#include <epoxy/gl.h>

struct _TacoGLPreviewPrivate {
    GLuint program;
    GLuint vao;
    GLuint vbo;
};

typedef struct _TacoGLPreviewPrivate TacoGLPreviewPrivate;

G_DEFINE_FINAL_TYPE_WITH_PRIVATE(TacoGLPreview,
                                 taco_gl_preview,
                                 GTK_TYPE_GL_AREA)

static gboolean
taco_gl_preview_render(GtkGLArea *gl_area, GdkGLContext *context);

static void
taco_gl_preview_resize(GtkGLArea *gl_area, int width, int height);

static void
taco_gl_preview_realize(GtkWidget *widget);

static void
taco_gl_preview_class_init(TacoGLPreviewClass *klass)
{
    GtkWidgetClass *const widget_class = GTK_WIDGET_CLASS(klass);
    GtkGLAreaClass *const gl_area_class = GTK_GL_AREA_CLASS(klass);

    gl_area_class->render = taco_gl_preview_render;
    gl_area_class->resize = taco_gl_preview_resize;
    widget_class->realize = taco_gl_preview_realize;
}

static void
taco_gl_preview_init(TacoGLPreview *self)
{
    TacoGLPreviewPrivate *const priv = taco_gl_preview_get_instance_private(self);
    GtkGLArea *const gl_area = GTK_GL_AREA(self);

    gtk_gl_area_set_allowed_apis(gl_area, GDK_GL_API_GL);
    gtk_gl_area_set_required_version(gl_area, 3, 3);
    /* gtk_gl_area_set_auto_render(GTK_GL_AREA(self), FALSE); */

    priv->program = 0;
    priv->vao = 0;
    priv->vbo = 0;
}

GtkWidget*
taco_gl_preview_new(void)
{

    return g_object_new(TACO_GL_PREVIEW_TYPE, NULL);
}

static gboolean
taco_gl_preview_render(GtkGLArea *gl_area, GdkGLContext *context)
{
    (void)context;
    (void)gl_area;

    glClearColor(0.5f, 0.5f, 0.5f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    return TRUE;
}

static void
taco_gl_preview_resize(GtkGLArea *gl_area, int width, int height)
{
    (void)gl_area;

    glViewport(0, 0, width, height);
}

static void
taco_gl_preview_realize(GtkWidget *widget)
{
    GtkGLArea *const gl_area = GTK_GL_AREA(widget);

    GTK_WIDGET_CLASS(taco_gl_preview_parent_class)->realize(widget);

    gtk_gl_area_make_current(gl_area);

    if (gtk_gl_area_get_error(gl_area) != NULL) {
        g_critical("Failed to make GL context current");
        return;
    }
}
