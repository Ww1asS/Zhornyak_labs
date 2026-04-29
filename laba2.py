import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView

class GISApplication:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ГИС Приложение - Достопримечательности Москвы")
        self.window.geometry("1400x900")

        self.markers = []
        self.polygons = []
        self.paths = []

        self.create_interface()

    def create_interface(self):
        control_frame = tk.Frame(self.window, bg="lightgray", height=100)
        control_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(control_frame, text="Координаты (широта,долгота):", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)

        self.coord_entry = tk.Entry(control_frame, width=25)
        self.coord_entry.grid(row=0, column=1, padx=5, pady=5)
        self.coord_entry.insert(0, "55.7558,37.6173")  # Координаты Москвы

        tk.Label(control_frame, text="Тип объекта:", bg="lightgray").grid(row=0, column=2, padx=5, pady=5)
        self.object_type = ttk.Combobox(control_frame, values=["Маркер", "Линия", "Полигон"])
        self.object_type.grid(row=0, column=3, padx=5, pady=5)
        self.object_type.set("Маркер")

        tk.Label(control_frame, text="Название:", bg="lightgray").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(control_frame, width=25)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(control_frame, text="Добавить объект", command=self.add_object, bg="lightblue")
        self.add_button.grid(row=1, column=2, padx=5, pady=5)

        self.clear_button = tk.Button(control_frame, text="Очистить все", command=self.clear_all, bg="lightcoral")
        self.clear_button.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(control_frame, text="Тип карты:", bg="lightgray").grid(row=2, column=0, padx=5, pady=5)
        self.osm_button = tk.Button(control_frame, text="OpenStreetMap", command=self.set_osm_map, bg="lightgreen")
        self.osm_button.grid(row=2, column=1, padx=5, pady=5)

        self.google_button = tk.Button(control_frame, text="Google Maps", command=self.set_google_map, bg="orange")
        self.google_button.grid(row=2, column=2, padx=5, pady=5)

        self.info_label = tk.Label(control_frame, text="ГИС система готова к работе", bg="lightgray", fg="blue")
        self.info_label.grid(row=2, column=3, padx=5, pady=5)

        self.map_widget = TkinterMapView(self.window, width=1380, height=700, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

        self.set_google_map()
        self.map_widget.set_position(55.7558, 37.6173)  # Центр Москвы
        self.map_widget.set_zoom(11)

        self.map_widget.add_right_click_menu_command(
            label="Добавить маркер здесь",
            command=self.add_marker_at_position,
            pass_coords=True
        )

        self.add_demo_objects()

    def set_osm_map(self):
        """Установка OpenStreetMap"""
        self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        self.info_label.config(text="Используется: OpenStreetMap")

    def set_google_map(self):
        """Установка Google Maps"""
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.info_label.config(text="Используется: Google Maps")

    def add_object(self):
        """Добавление объекта на карту"""
        try:
            coords_text = self.coord_entry.get()
            name = self.name_entry.get() or "Объект"
            lat, lon = map(float, coords_text.split(','))
            obj_type = self.object_type.get()

            if obj_type == "Маркер":
                marker = self.map_widget.set_marker(lat, lon, text=name)
                self.markers.append(marker)
                self.info_label.config(text=f"Добавлен маркер: {name}")

            elif obj_type == "Линия":
                # Для линии нужно минимум 2 точки
                if len(self.markers) >= 1:
                    end_lat, end_lon = lat + 0.01, lon + 0.01
                    path = self.map_widget.set_path([(lat, lon), (end_lat, end_lon)])
                    self.paths.append(path)
                    self.info_label.config(text=f"Добавлена линия: {name}")
                else:
                    self.info_label.config(text="Для линии нужно больше точек")

            elif obj_type == "Полигон":
                # Создаем простой треугольник
                polygon_coords = [
                    (lat, lon),
                    (lat + 0.005, lon + 0.005),
                    (lat + 0.005, lon - 0.005),
                    (lat, lon)
                ]
                polygon = self.map_widget.set_polygon(polygon_coords, name=name)
                self.polygons.append(polygon)
                self.info_label.config(text=f"Добавлен полигон: {name}")

        except ValueError:
            self.info_label.config(text="Ошибка: неверный формат координат")
        except Exception as e:
            self.info_label.config(text=f"Ошибка: {str(e)}")

    def add_marker_at_position(self, coords):
        """Добавление маркера по клику правой кнопкой мыши"""
        marker = self.map_widget.set_marker(coords[0], coords[1], text=f"Маркер {len(self.markers) + 1}")
        self.markers.append(marker)
        self.info_label.config(text=f"Добавлен маркер в позиции: {coords}")

    def add_demo_objects(self):
        """Добавление демонстрационных объектов"""
        # 1. ТОЧЕЧНЫЕ ОБЪЕКТЫ (маркеры) - 3 объекта
        mgu = self.map_widget.set_marker(55.7023, 37.5328, text="МГУ")
        mai = self.map_widget.set_marker(55.8118, 37.5266, text="МАИ")
        bmstu = self.map_widget.set_marker(55.7665, 37.6844, text="МГТУ им. Баумана")
        self.markers.extend([mgu, mai, bmstu])

        # 2. ЛИНЕЙНЫЕ ОБЪЕКТЫ - 3 объекта
        # Ломоносовский проспект от МГУ
        lomonosov_route = self.map_widget.set_path([
            (55.7023, 37.5328),  # МГУ
            (55.7098, 37.5512),
            (55.7190, 37.5710)
        ])

        # Ленинградский проспект от МАИ
        leningradsky_route = self.map_widget.set_path([
            (55.8118, 37.5266),  # МАИ
            (55.7970, 37.5530),
            (55.7810, 37.5810)
        ])

        # Линия метро через Бауманскую
        metro_route = self.map_widget.set_path([
            (55.7558, 37.6173),
            (55.7665, 37.6844),  # МГТУ
            (55.7735, 37.7024)
        ])

        self.paths.extend([lomonosov_route, leningradsky_route, metro_route])

        # 3. ПЛОЩАДНЫЕ ОБЪЕКТЫ (полигоны) - 3 объекта
        # Территория МГУ
        mgu_campus = self.map_widget.set_polygon([
            (55.7050, 37.5280),
            (55.7050, 37.5380),
            (55.6996, 37.5380),
            (55.6996, 37.5280),
            (55.7050, 37.5280)
        ], name="Территория МГУ", fill_color="lightblue", outline_color="darkblue")

        # Территория МАИ
        mai_campus = self.map_widget.set_polygon([
            (55.8140, 37.5240),
            (55.8140, 37.5290),
            (55.8096, 37.5290),
            (55.8096, 37.5240),
            (55.8140, 37.5240)
        ], name="Территория МАИ", fill_color="lightgreen", outline_color="darkgreen")

        # Парк Горького
        gorky_park = self.map_widget.set_polygon([
            (55.7310, 37.6010),
            (55.7310, 37.6120),
            (55.7250, 37.6120),
            (55.7250, 37.6010),
            (55.7310, 37.6010)
        ], name="Парк Горького", fill_color="lightgreen", outline_color="green")

        self.polygons.extend([mgu_campus, mai_campus, gorky_park])

        self.info_label.config(text="Демонстрационные объекты добавлены: 3 маркера, 3 линии, 3 полигона")

    def clear_all(self):
        """Очистка всех объектов с карты"""
        for marker in self.markers:
            marker.delete()
        for polygon in self.polygons:
            polygon.delete()
        for path in self.paths:
            path.delete()

        self.markers.clear()
        self.polygons.clear()
        self.paths.clear()

        self.info_label.config(text="Все объекты удалены")

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = GISApplication()
    app.run()
