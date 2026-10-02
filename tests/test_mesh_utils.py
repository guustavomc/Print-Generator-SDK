import pytest
import trimesh

from print_generator_sdk import MeshValidationError, build_result, validate


def test_valid_box_passes():
    result = build_result(trimesh.creation.box(extents=(10, 20, 30)))
    assert result.is_watertight
    assert result.dimensions_mm == pytest.approx((10, 20, 30))
    assert result.volume_cm3 == pytest.approx(6.0)
    assert result.stl_bytes[:5] != b"solid"  # STL binário


def test_open_mesh_fails():
    box = trimesh.creation.box(extents=(10, 10, 10))
    box.update_faces(list(range(len(box.faces) - 1)))  # remove um triângulo
    with pytest.raises(MeshValidationError, match="watertight"):
        validate(box)


def test_bed_size_is_configurable():
    box = trimesh.creation.box(extents=(300, 10, 10))
    with pytest.raises(MeshValidationError, match="eixo X"):
        build_result(box)
    assert build_result(box, bed_size=(350, 350, 350)).is_watertight