import Rhino.Geometry as rg

# ۱. متغیرهای پارامتریک برج
width = 16.0
length = 26.0
floors = 7
floor_height = 3.0
total_height = floors * floor_height # ۲۱ متر

# ۲. ساخت منحنی پایه و سقف طبقات (Slabs)
base_plane = rg.Plane.WorldXY
base_rect = rg.Rectangle3d(base_plane, width, length)
base_curve = base_rect.ToNurbsCurve()

slabs = []
for i in range(floors + 1):
    z_offset = i * floor_height
    move_vector = rg.Vector3d(0, 0, z_offset)
    floor_curve = base_curve.Duplicate()
    floor_curve.Translate(move_vector)
    planar_surfaces = rg.Brep.CreatePlanarBreps(floor_curve)
    if planar_surfaces:
        slabs.append(planar_surfaces[0])

# ۳. ساخت حجم کل دور برج (Building Mass)
building_mass = rg.Extrusion.Create(base_curve, total_height, True)

# ۴. تولید بردار تابش خورشید (Sun Vector) بالای برج
center_roof = rg.Point3d(width / 2.0, length / 2.0, total_height)
sun_point = rg.Point3d(center_roof.X + 10.0, center_roof.Y + 10.0, center_roof.Z + 15.0)
sun_ray = rg.Line(sun_point, center_roof)

# ۵. تنظیم خروجی‌ها (نیاز به ۳ خروجی a, b, c روی کامپوننت داری)
a = slabs          # خروجی A: سقف طبقات
b = building_mass  # خروجی B: پوسته سه‌بعدی برج
c = sun_ray        # خروجی C: خط تابش خورشید
