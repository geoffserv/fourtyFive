from helm import Helm
from helm_shapes import Shape, ShapeNotesList


def test_helm_top_level():
    # pytest assertion
    helm_test_instance = Helm(init_gfx=False)
    # Top level health check - everything initialized and there is at least
    # 1 control surface
    assert len(helm_test_instance.controlSurfaces) > 0


def test_shape():
    shape_test_instance = Shape(canvas_margin=10)
    shape_test_instance.coordinates = [(1, 2)]
    shape_test_instance.degrees = [90]
    shape_test_instance.coordinates_boxes = [(20, 40, 80, 90)]
    assert shape_test_instance.coordinates[0] == (1, 2)
    assert shape_test_instance.degrees[0] == 90
    assert shape_test_instance.coordinates_boxes[0] == (20, 40, 80, 90)


def test_shapenoteslist():
    shapenoteslist_test_instance = ShapeNotesList(canvas_margin=10,
                                                  spacing_width=44,
                                                  line_spacing=2,
                                                  left_margin=226)
