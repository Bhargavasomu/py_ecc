from functools import lru_cache

from py_ecc.bls12_381_curve import (
    bls12_381,
    optimized_bls12_381,
)

from py_ecc.bn128_curve import (
    bn128,
    optimized_bn128,
)

from py_ecc.curve_properties import (
    curve_properties,
    optimized_curve_properties,
)

from py_ecc.field_properties import (
    field_properties,
)


def validate_field_properties() -> None:
    for curve_name in field_properties:
        # Check if field_modulus is prime
        field_modulus = field_properties[curve_name]["field_modulus"]
        if pow(2, field_modulus, field_modulus) != 2:
            raise ValueError(
                "Field Modulus of the curve {} is not a prime".format(curve_name)
            )


def validate_curve_properties() -> None:
    for curve_name in curve_properties:
        # Check if curve_order is prime
        curve_order = curve_properties[curve_name]["curve_order"]
        if pow(2, curve_order, curve_order) != 2:
            raise ValueError(
                "Curve Order of the curve {} is not a prime".format(curve_name)
            )

        # Check consistency b/w field_modulus and curve_order
        field_modulus = field_properties[curve_name]["field_modulus"]
        if (field_modulus ** 12 - 1) % curve_order != 0:
            raise ValueError(
                "Inconsistent values among field_modulus and curve_order in the curve {}"
                .format(curve_name)
            )

        # Check validity of pseudo_binary_encoding
        pseudo_binary_encoding = curve_properties[curve_name]["pseudo_binary_encoding"]
        ate_loop_count = curve_properties[curve_name]["ate_loop_count"]
        if sum([e * 2**i for i, e in enumerate(pseudo_binary_encoding)]) != ate_loop_count:
            raise ValueError(
                "Inconsistent values among pseudo_binary_encoding and ate_loop_count"
            )


def validate_optimized_curve_properties() -> None:
    for curve_name in optimized_curve_properties:
        # Check if curve_order is prime
        curve_order = optimized_curve_properties[curve_name]["curve_order"]
        if pow(2, curve_order, curve_order) != 2:
            raise ValueError(
                "Curve Order of the optimized curve {} is not a prime".format(curve_name)
            )

        # Check consistency b/w field_modulus and curve_order
        field_modulus = field_properties[curve_name]["field_modulus"]
        if (field_modulus ** 12 - 1) % curve_order != 0:
            raise ValueError(
                "Inconsistent values among field_modulus and curve_order in the optimized curve {}"
                .format(curve_name)
            )

        # Check validity of pseudo_binary_encoding
        pseudo_binary_encoding = optimized_curve_properties[curve_name]["pseudo_binary_encoding"]
        ate_loop_count = optimized_curve_properties[curve_name]["ate_loop_count"]
        if sum([e * 2**i for i, e in enumerate(pseudo_binary_encoding)]) != ate_loop_count:
            raise ValueError(
                "Inconsistent values among pseudo_binary_encoding and ate_loop_count"
                "in the optimized curve {}"
                .format(curve_name)
            )


def validate_generators() -> None:
    # Validate generators of normal curves
    for curve_obj in (bn128, bls12_381):
        if not curve_obj.is_on_curve(curve_obj.G1, curve_obj.b):
            raise ValueError(
                "G1 doesn't lie on the curve {} defined by b".format(curve_obj.curve_name)
            )

        if not curve_obj.is_on_curve(curve_obj.G2, curve_obj.b2):
            raise ValueError(
                "G2 doesn't lie on the curve {} defined by b2".format(curve_obj.curve_name)
            )

        if not curve_obj.is_on_curve(curve_obj.G12, curve_obj.b12):
            raise ValueError(
                "G12 doesn't lie on the curve {} defined by b12".format(curve_obj.curve_name)
            )

    # Validate generators of optimized curves
    for optimized_curve_obj in (optimized_bn128, optimized_bls12_381):
        if not optimized_curve_obj.is_on_curve(optimized_curve_obj.G1, optimized_curve_obj.b):
            raise ValueError(
                "G1 doesn't lie on the optimized curve {} defined by b"
                .format(optimized_curve_obj.curve_name)
            )

        if not optimized_curve_obj.is_on_curve(optimized_curve_obj.G2, optimized_curve_obj.b2):
            raise ValueError(
                "G2 doesn't lie on the optimized curve {} defined by b2"
                .format(optimized_curve_obj.curve_name)
            )

        if not optimized_curve_obj.is_on_curve(optimized_curve_obj.G12, optimized_curve_obj.b12):
            raise ValueError(
                "G12 doesn't lie on the optimized curve {} defined by b12"
                .format(optimized_curve_obj.curve_name)
            )


@lru_cache(maxsize=1)
def validate_constants() -> None:
    """
    This function validates the constants that are being used throughout
    the whole codebase. It specifically verifies the curve and field properties
    """
    validate_field_properties()
    validate_curve_properties()
    validate_optimized_curve_properties()
    validate_generators()