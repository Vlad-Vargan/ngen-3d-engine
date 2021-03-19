import numpy as np

from ..parser.parsers import SimpleObjParser
from ..tool.tools import calc_rotation_matrix
from ..tool.tools import calc_translation_matrix
from ..tool.tools import calc_scaling_matrix
from ..tool.tools import parametrical_line_point

class Model:
    def __init__(self,
    	         pos_x=None,
    	         pos_y=None,
    	         pos_z=None, 
    	         angle_x_deg=None,
    	         angle_y_deg=None,
    	         angle_z_deg=None,
    	         scale_x=None,
    	         scale_y=None,
    	         scale_z=None):
        if pos_x is None:
            pos_x = 0

        if pos_y is None:
            pos_y = 0

        if pos_z is None:
            pos_z = 0

        if angle_x_deg is None:
            angle_x_deg = 0

        if angle_y_deg is None:
            angle_y_deg = 0

        if angle_z_deg is None:
            angle_z_deg = 0

        if scale_x is None:
            scale_x = 1

        if scale_y is None:
            scale_y = 1

        if scale_z is None:
            scale_z = 1

        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pos_z = pos_z
        self._angle_x_deg = angle_x_deg
        self._angle_y_deg = angle_y_deg
        self._angle_z_deg = angle_z_deg
        self._scale_x = scale_x
        self._scale_y = scale_y
        self._scale_z = scale_z
        self._vertexes = None
        self._normals = None
        self._surfaces = None
        self._points = None

    @property
    def pos_x(self):
    	return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value

    @property
    def pos_y(self):
    	return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value

    @property
    def pos_z(self):
    	return self._pos_z

    @pos_z.setter
    def pos_z(self, value):
        self._pos_z = value

    @property
    def angle_x_deg(self):
    	return self._angle_x_deg

    @angle_x_deg.setter
    def angle_x_deg(self, value):
        self._angle_x_deg = value

    @property
    def angle_y_deg(self):
    	return self._angle_y_deg

    @angle_y_deg.setter
    def angle_y_deg(self, value):
        self._angle_y_deg = value

    @property
    def angle_z_deg(self):
    	return self._angle_z_deg

    @angle_z_deg.setter
    def angle_z_deg(self, value):
        self._angle_z_deg = value

    @property
    def scale_x(self):
    	return self._scale_x

    @scale_x.setter
    def scale_x(self, value):
        self._scale_x = value

    @property
    def scale_y(self):
    	return self._scale_y

    @scale_y.setter
    def scale_y(self, value):
        self._scale_y = value

    @property
    def scale_z(self):
    	return self._scale_z

    @scale_z.setter
    def scale_z(self, value):
        self._scale_z = value 

    @property
    def points(self):
    	return self._points

    def move_x(self, value):
        self._pos_x += value

    def move_y(self, value):
        self._pos_y += value

    def move_z(self, value):
        self._pos_z -= value

    def rotate_x(self, value):
        self._angle_x_deg += value

    def rotate_y(self, value):
        self._angle_y_deg += value

    def rotate_z(self, value):
        self._angle_z_deg += value

    def update(self):
        pass

class DummyCubeModel(Model):
    def __init__(self,
    	         pos_x=None,
    	         pos_y=None,
    	         pos_z=None, 
    	         angle_x_deg=None,
    	         angle_y_deg=None,
    	         angle_z_deg=None,
    	         scale_x=None,
    	         scale_y=None,
    	         scale_z=None):
        super().__init__(pos_x,
                         pos_y,
                         pos_z,
                         angle_x_deg,
                         angle_y_deg,
                         angle_z_deg,
                         scale_x,
                         scale_y,
                         scale_z)


        self._calculate_cube_coordinates()

    def _calculate_cube_coordinates(self):
        delta = 1
        center_x = 0
        center_y = 0
        center_z = 0

        point_1 = np.array([center_x + delta, center_y + delta, center_z + delta, 1])
        point_2 = np.array([center_x - delta, center_y + delta, center_z + delta, 1])
        point_3 = np.array([center_x + delta, center_y - delta, center_z + delta, 1])
        point_4 = np.array([center_x - delta, center_y - delta, center_z + delta, 1])
        point_5 = np.array([center_x + delta, center_y + delta, center_z - delta, 1])
        point_6 = np.array([center_x - delta, center_y + delta, center_z - delta, 1])
        point_7 = np.array([center_x + delta, center_y - delta, center_z - delta, 1])
        point_8 = np.array([center_x - delta, center_y - delta, center_z - delta, 1])

        self._vertexes = np.array([point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8])

    def update(self):
        scaling_matrix = calc_scaling_matrix(self._scale_x,
                                             self._scale_y,
                                             self._scale_z)

        rotation_matrix = calc_rotation_matrix(self._angle_x_deg,
                                               self._angle_y_deg,
                                               self._angle_z_deg)

        translation_matrix = calc_translation_matrix(self._pos_x,
                                                     self._pos_y,
                                                     self._pos_z)

        transform_matrix = np.matmul(translation_matrix, rotation_matrix)

        self._points = np.matmul(self._vertexes, scaling_matrix.T)
        self._points = np.matmul(self._points[:,:], transform_matrix.T)


        

        


class ObjModel(Model):
    def __init__(self,
                 obj_file_path,
    	         pos_x=None,
    	         pos_y=None,
    	         pos_z=None, 
    	         angle_x_deg=None,
    	         angle_y_deg=None,
    	         angle_z_deg=None,
    	         scale_x=None,
    	         scale_y=None,
    	         scale_z=None):
        super().__init__(pos_x,
                         pos_y,
                         pos_z,
                         angle_x_deg,
                         angle_y_deg,
                         angle_z_deg,
                         scale_x,
                         scale_y,
                         scale_z)
        self._coordinate_axe_line_x = None
        self._coordinate_axe_line_y = None
        self._coordinate_axe_line_z = None
        self._normal_lines = None
        self._normal_lines_default = None
        self._normals = None
        self._vertexes = None
        self._surfaces = None
        self._center = np.zeros((3,))

        self._parser = SimpleObjParser(obj_file_path)
        self._obj_file_path = obj_file_path

        self._load_from_obj()
        self._calculate_center()
        self._translate_to_center()
        self._calc_normal_lines()

    @property
    def center(self):
    	return self._center

    @center.setter
    def center(self, value):
        self._center = value

    @property
    def center_x(self):
    	return self._center[0]

    @center_x.setter
    def center_x(self, value):
        self._center[0] = value

    @property
    def center_y(self):
    	return self._center[1]
    
    @center_y.setter
    def center_y(self, value):
        self._center[1] = value

    @property
    def center_z(self):
    	return self._center[2]

    @center_z.setter
    def center_z(self, value):
        self._center[2] = value
    
    def _calculate_center(self):
        center = None

        xs = self._vertexes[:,0]
        ys = self._vertexes[:,1]
        zs = self._vertexes[:,2]

        self.center_x = np.mean(xs)
        self.center_y = np.mean(ys)
        self.center_z = np.mean(zs)

        self._center = np.array([self.center_x, self.center_y, self.center_z])

    def _calc_normal_lines(self):
        self._normal_lines_default = np.ones((self._surfaces.shape[0] * 3, 2, 4))
        self._normal_lines = np.ones((self._surfaces.shape[0] * 3, 2, 4))

        for i in range(0, len(self._surfaces), 1):
            surface = self._surfaces[i]
            contour_normals = (self._normals[surface[:,1].astype(int) - 1])
            contour_points = self._vertexes[surface[:,0].astype(int) - 1]

            for j, (normal, start_point) in enumerate(zip(contour_normals, contour_points)):
                end_point = parametrical_line_point(start_point, normal, 0.2)
                normal_line = np.array([start_point, end_point])

                self._normal_lines_default[i*3 + j] = normal_line


    def _translate_to_center(self):
        translation_matrix = calc_translation_matrix(-self.center_x,
                                                     -self.center_y,
                                                     -self.center_z)
        self._vertexes = np.matmul(self._vertexes[:, :], translation_matrix.T)
    
    
    def _load_from_obj(self):
        vertexes, normals, surfaces = self._parser.parse()

        self._vertexes = vertexes
        self._normals = normals
        self._normals_default = normals
        self._surfaces = surfaces

    def _update_normals(self, transform_matrix):
        self._normals = np.matmul(self._normals_default[:,:], np.linalg.inv(transform_matrix))

    def _update_points(self, transform_matrix):
        self._points = np.matmul(self._vertexes[:,:], transform_matrix.T)

    def _update_normal_lines(self, transform_matrix):
        for i, normal_line in enumerate(self._normal_lines_default):
            points = normal_line
            
            self._normal_lines[i] = np.matmul(points, transform_matrix.T)


    def update(self):
        scaling_matrix = calc_scaling_matrix(self._scale_x,
                                             self._scale_y,
                                             self._scale_z)

        rotation_matrix = calc_rotation_matrix(self._angle_x_deg,
                                               self._angle_y_deg,
                                               self._angle_z_deg)

        translation_matrix = calc_translation_matrix(self._pos_x,
                                                     self._pos_y,
                                                     self._pos_z)
        
        transform_matrix = np.matmul(rotation_matrix, scaling_matrix)
        transform_matrix = np.matmul(translation_matrix, transform_matrix)


        self._update_normals(transform_matrix)
        self._update_points(transform_matrix)
        self._update_normal_lines(transform_matrix)
        
    
