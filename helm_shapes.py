import math


class ShapeNotesList(object):
    def __init__(self, spacing_width, canvas_margin=10, line_spacing=0,
                 left_margin=0):
        self.spacing_width = spacing_width
        self.canvas_margin = canvas_margin
        self.line_spacing = line_spacing
        self.left_margin = left_margin
        # list of coordinates representing this shape
        self.coordinates = []
        self.degrees = []
        self.coordinates_boxes = []
        self.find_coordinates()

    def find_coordinates(self):
        for i in range(1, 13):
            self.coordinates.append(
                (
                    self.canvas_margin + self.left_margin +
                    (i * self.spacing_width),
                    self.canvas_margin + self.spacing_width + self.line_spacing
                )
            )
            self.degrees.append(0)
            self.coordinates_boxes.append(
                (
                    self.canvas_margin +
                    (i * self.spacing_width) - int(self.spacing_width/2) +
                    self.left_margin,
                    self.canvas_margin +
                    self.spacing_width - int(self.spacing_width/2) +
                    self.line_spacing,
                    self.spacing_width,  # width
                    self.spacing_width   # height
                )
            )


class ShapeWheel(object):
    def __init__(self, canvas_size, r, slice_no=1, offset_degrees=0,
                 canvas_margin=10):
        self.slice_no = int(slice_no)
        self.r = int(r)
        self.circle_divisions = 12  # 12-slices around the circle
        self.offset_degrees = int(offset_degrees)
        self.canvas_margin = int(canvas_margin)
        self.origin_x = int(
            (canvas_size / 2) + self.canvas_margin)  # Center of the canvas X
        self.origin_y = int(
            (canvas_size / 2) + self.canvas_margin)  # Center of the canvas Y
        self.canvas_width = (canvas_size + (self.canvas_margin * 2))
        self.canvas_height = (canvas_size + (self.canvas_margin * 2))

        # offset_orientation is a number of degrees added to everything
        # to set an overall coordinate system orientation
        self.offset_orientation = 90

        # list of coordinates representing this shape
        self.coordinates = []
        # associates list of degrees from the origin for each coordinate pair
        self.degrees = []
        self.find_coordinates()

    def find_coordinates(self):
        for i in range(12):
            self.coordinates.append(
                # One corner of the triangle along the circle radius r,
                # at sliceNo*1/12circle
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
            self.degrees.append(
                int(-((360 / self.circle_divisions) * i))
                - self.offset_degrees
            )


class ShapeWheelSlice(ShapeWheel):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at sliceNo*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at (sliceNo+1)*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )


class ShapeWheelRay(ShapeWheel):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )
