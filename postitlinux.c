
#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>

#define FILENAME "postit.ini"

GtkWidget *text_view;
//gcc -o postit_app postit_app.c `pkg-config --cflags --libs gtk+-3.0`
void load_text_from_file(GtkTextBuffer *buffer, const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file) {
        fseek(file, 0, SEEK_END);
        long fsize = ftell(file);
        fseek(file, 0, SEEK_SET);

        char *text = malloc(fsize + 1);
        fread(text, 1, fsize, file);
        text[fsize] = 0;

        gtk_text_buffer_set_text(buffer, text, -1);

        free(text);
        fclose(file);
    }
}

void save_text_to_file(GtkTextBuffer *buffer, const char *filename) {
    GtkTextIter start, end;
    gtk_text_buffer_get_start_iter(buffer, &start);
    gtk_text_buffer_get_end_iter(buffer, &end);

    char *text = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);

    FILE *file = fopen(filename, "w");
    if (file) {
        fwrite(text, 1, strlen(text), file);
        fclose(file);
    }
    g_free(text);
}

static void on_destroy(GtkWidget *widget, gpointer data) {
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
    save_text_to_file(buffer, FILENAME);
    gtk_main_quit();
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Post-It");
    gtk_window_set_default_size(GTK_WINDOW(window), 500, 500);
    g_signal_connect(window, "destroy", G_CALLBACK(on_destroy), NULL);

    GtkWidget *scrolled_window = gtk_scrolled_window_new(NULL, NULL);
    gtk_scrolled_window_set_policy(GTK_SCROLLED_WINDOW(scrolled_window), GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);
    gtk_container_add(GTK_CONTAINER(window), scrolled_window);

    text_view = gtk_text_view_new();
    gtk_container_add(GTK_CONTAINER(scrolled_window), text_view);

    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
    load_text_from_file(buffer, FILENAME);

    // Definir a cor de fundo para amarelo
    GdkRGBA yellow = {1, 1, 0, 1};
    gtk_widget_override_background_color(text_view, GTK_STATE_FLAG_NORMAL, &yellow);

    gtk_widget_show_all(window);

    gtk_main();

    return 0;
}
