import flet as ft
import base64
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
brightness_value = 1.0
contrast_value = 1.0
sharpness_value = 0.0


def main(page: ft.Page):
    global brightness_value, contrast_value, sharpness_value

    def on_change_brightness(e):
        global brightness_value
        brightness_value = float(e.control.value) / 50

    def on_change_contrast(e):
        global contrast_value
        contrast_value = float(e.control.value) / 50

    def on_change_sharpness(e):
        global sharpness_value
        sharpness_value = float(e.control.value) / 50

    img = ft.Image(
        border_radius=ft.border_radius.all(20)
    )

    def update_timer():
        while True:
            _, frame = cap.read()

            # Apply brightness and contrast
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv = np.array(hsv, dtype=np.float64)
            hsv[:, :, 2] = hsv[:, :, 2] * brightness_value
            hsv[:, :, 2][hsv[:, :, 2] > 255] = 255
            hsv = np.array(hsv, dtype=np.uint8)
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            frame = cv2.convertScaleAbs(frame, alpha=contrast_value, beta=0)

            # Apply sharpness
            if sharpness_value > 0:
                kernel = np.array([[0, -sharpness_value, 0],
                                   [-sharpness_value, 1 + 4 * sharpness_value, -sharpness_value],
                                   [0, -sharpness_value, 0]])
                frame = cv2.filter2D(frame, -1, kernel)

            _, im_arr = cv2.imencode('.png', frame)
            im_b64 = base64.b64encode(im_arr)
            img.src_base64 = im_b64.decode("utf-8")
            img.update()

    page.padding = 50
    page.window_left = page.window_left + 100
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.Container(
            margin=ft.margin.only(bottom=40),
            content=ft.Row([
                ft.Card(
                    elevation=30,
                    content=ft.Container(
                        bgcolor=ft.colors.WHITE24,
                        padding=10,
                        border_radius=ft.border_radius.all(20),
                        content=ft.Column([
                            img,
                            ft.Text("Live Camera feed",
                                    size=20, weight="bold",
                                    color=ft.colors.BLUE),
                        ]
                        ),
                    )
                ),
                ft.Card(
                    elevation=30,
                    content=ft.Container(
                        bgcolor=ft.colors.WHITE24,
                        padding=10,
                        border_radius=ft.border_radius.all(20),
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.BRIGHTNESS_6),
                                ft.Slider(min=0, max=100, value=50, on_change=on_change_brightness)]
                            ),
                            ft.Row([
                                ft.Icon(ft.icons.CONTRAST),
                                ft.Slider(min=0, max=100, value=50, on_change=on_change_contrast)]
                            ),
                            ft.Row([
                                ft.Icon(ft.icons.ADD_SHARP),
                                ft.Slider(min=0, max=100, value=50, on_change=on_change_sharpness)]
                            )

                        ]
                        ),

                    )
                )
            ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
    )
    page.run_thread(update_timer)


if __name__ == '__main__':
    ft.app(target=main)
    cap.release()
    cv2.destroyAllWindows()
