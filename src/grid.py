"""
Defines classes needed for the grid as well as useful methods surrounding it.
"""


from dataclasses import dataclass, field
from pathlib import Path
from itertools import product
import numpy as np
import bpy
import bmesh

@dataclass
class GridFrame:
    """
    Represents the physical grid seen in the rendered Blender scene.
    """

    origin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    shape: tuple[int, int, int] = (3, 3, 3)
    cell_size: float = 1.5
    beam_thickness: float = 0.010
    wall_thickness: float = 0.025
    root_name: str = "GridFrameRoot"
    walls: list[bpy.types.Object] = field(default_factory=list, init=False)
    beams: list[bpy.types.Object] = field(default_factory=list, init=False)
    root: bpy.types.Object | None = field(default=None, init=False)

    def build(self, collection: bpy.types.Collection | None = None) -> None:
        """Builds a 3D grid wireframe in Blender."""

        # clear grid if already existing
        self.clear()

        bt = self.beam_thickness
        wt = self.wall_thickness

        # create root object and link to collection
        target_col = collection or bpy.context.scene.collection
        root_obj = bpy.data.objects.new(self.root_name, None)
        root_obj.location = self.origin
        target_col.objects.link(root_obj)
        self.root = root_obj

        # remove default cube
        cube = bpy.data.objects.get("Cube")
        if cube is not None:
            bpy.data.objects.remove(cube, do_unlink=True)

        ## build walls
        walls = []
        wall_size = max(self.shape) * self.cell_size * 10

        back_mesh = create_box_mesh(name="wback", size=(wt, wall_size, wall_size))
        back_wall = make_obj_from_mesh(back_mesh)
        back_wall.location = (-(bt+wt)/2, 0.0, 0.0)
        walls.append(back_wall)

        bot_mesh = create_box_mesh(name="wbot", size=(wall_size, wall_size, wt))
        bot_wall = make_obj_from_mesh(bot_mesh)
        bot_wall.location = (0.0, 0.0, -(bt+wt)/2)
        walls.append(bot_wall)

        for wall in walls:
            wall.parent = root_obj
            target_col.objects.link(wall)
        self.walls = walls

        ## build beams
        hx, hy, hz = np.asarray(self.shape) * self.cell_size

        # build origin beams first
        beams = []

        m_origx = create_box_mesh(name="origx", size=(hx+bt, bt, bt))
        b_origx = make_obj_from_mesh(m_origx)
        b_origx.location = (hx/2.0, 0.0, 0.0)
        beams.append(b_origx)

        m_origy = create_box_mesh(name="origy", size=(bt, hy+bt, bt))
        b_origy = make_obj_from_mesh(m_origy)
        b_origy.location = (0.0, hy/2.0, 0.0)
        beams.append(b_origy)

        m_origz = create_box_mesh(name="origz", size=(bt, bt, hz+bt))
        b_origz = make_obj_from_mesh(m_origz)
        b_origz.location = (0.0, 0.0, hz/2.0)
        beams.append(b_origz)

        # build other beams per orientation
        nx, ny, nz = self.shape

        for i in range(1, nx+1):
            this_mesh = create_box_mesh(name=f"beam{i}onxdiry", size=(bt, hy+bt, bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (self.cell_size*i, hy/2, 0.0)
            beams.append(this_beam)

            this_mesh = create_box_mesh(name=f"beam{i}onxdirz", size=(bt, bt, hz+bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (self.cell_size*i, 0.0, hz/2)
            beams.append(this_beam)

        for i in range(1, ny+1):
            this_mesh = create_box_mesh(name=f"beam{i}onydirx", size=(hx+bt, bt, bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (hx/2, self.cell_size*i, 0.0)
            beams.append(this_beam)

            this_mesh = create_box_mesh(name=f"beam{i}onydirz", size=(bt, bt, hz+bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (0.0, self.cell_size*i, hz/2)
            beams.append(this_beam)

        for i in range(1, nz+1):
            this_mesh = create_box_mesh(name=f"beam{i}onzdirx", size=(hx+bt, bt, bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (hx/2, 0.0, self.cell_size*i)
            beams.append(this_beam)

            this_mesh = create_box_mesh(name=f"beam{i}onzdiry", size=(bt, hy+bt, bt))
            this_beam = make_obj_from_mesh(this_mesh)
            this_beam.location = (0.0, hy/2, self.cell_size*i)          
            beams.append(this_beam)
            
        for beam in beams:
            beam.parent = root_obj
            target_col.objects.link(beam)
        self.beams = beams

        bpy.ops.wm.save_as_mainfile(filepath=str(Path("grid_test_new.blend").resolve()))

        return

    def clear(self):
        for obj in self.beams + self.walls:
            try:
                if obj is not None:
                    py.data.objects.remove(obj, do_unlink=True)
            except ReferenceError:
                pass
        self.beams = []
        self.walls = []

        try:
            if self.root is not None:
                bpy.data.objects.remove(self.root, do_unlink=True)
        except ReferenceError:
            pass
        self.root = None

        for obj in list(bpy.data.objects):
            if obj.name == self.root_name or obj.name.startswith(
                f"{self.root_name}."
            ):
                try:
                    bpy.data.objects.remove(obj, do_unlink=True)
                except ReferenceError:
                    pass
            
        return

def create_box_mesh(
        name: str,
        size: tuple[float, float, float]
) -> bpy.types.Mesh:
    """Create a mesh object for a box (e.g. beam or panel) of a given size."""
    sx, sy, sz = size

    box = bmesh.new()
    bmesh.ops.create_cube(box, size=1.0)
    bmesh.ops.scale(box, vec=(sx, sy, sz), verts=box.verts)

    mesh = bpy.data.meshes.new(name)
    box.to_mesh(mesh)
    box.free()

    return mesh

def make_obj_from_mesh(mesh: bpy.types.Mesh) -> bpy.types.Object:
    """Turn a mesh into a Blender object."""

    obj = bpy.data.objects.new(mesh.name, mesh)
    return obj

import bpy


def ensure_default_camera(
    name: str = "Camera",
    location: tuple[float, float, float] = (16.82, 7.24, 3.73),
    rotation_euler: tuple[float, float, float] = (1.45, 0.0, 1.91),
    rotation_mode: str = "XYZ",
    lens: float = 50.0,
    sensor_width: float = 36.0,
    sensor_fit: str = "AUTO",
) -> bpy.types.Object:
    """Sets the camera back to settings visually determined as optimal."""

    cam_obj = bpy.data.objects.get(name)

    cam_obj.rotation_mode = rotation_mode
    cam_obj.location = location
    cam_obj.rotation_euler = rotation_euler

    cam_obj.data.lens = lens
    cam_obj.data.sensor_width = sensor_width
    cam_obj.data.sensor_fit = sensor_fit

    bpy.context.scene.camera = cam_obj

    return cam_obj