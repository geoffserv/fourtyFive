from helm import *


def test_helm():
    # pytest assertion
    helm_test_instance = Helm(init_gfx=False)
    # Top level health check - everything initialized and there is at least 1 control surface
    assert len(helm_test_instance.controlSurfaces) > 0
