from gfxTest import *

def test_fourty_five():
    # pytest assertion
    fourtyFiveTestObj = None
    fourtyFiveTestObj = fourtyFive(initGfx=False)
    # Top level healthcheck - everything initialized and there is at least 1 control surface
    assert len(fourtyFiveTestObj.controlSurfaces) > 0
