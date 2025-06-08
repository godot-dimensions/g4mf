# G4MF Math

## Overview

Most online documentation, math literature, and code libraries focus on 2D and 3D math. A lot of this easily translates into 4D math, but a lot of it does not.

This section of the G4MF specification does not actually specify requirements for storing valid G4MF data. Instead, it provides guidance for implementations on how to actually compute the math needed to work with G4MF data.

## Calculating Perpendicular Vectors

In 3D, the cross product of two vectors produces a vector that is perpendicular to both input vectors, with the following properties:

- There are exactly 2 inputs (as with most products in math).
- The length of the output vector is the area of the parallelogram spanned by the input vectors.
- The orientation of the output vector is a unique vector perpendicular to the inputs, following the convention that the cross product of +X and +Y gives +Z.

We can extend the cross product to N-dimensional space if we discard one of these properties. If you want to find the area of the parallelogram spanned by only 2 vectors in N-dimensional space, there is a simple formula for that which preserves the first two properties. However, if you want to find a vector perpendicular to N-1 input vectors in N-dimensional space, you can use the following algorithm, which preserves the last two properties. The length of the vector will be the volume of the parallelepiped (or higher dimensional equivalent) spanned by all input vectors.

For 4D specifically, here is a special case that finds a 4th 4D vector perpendicular to 3 input 4D vectors:

<details>

Python:

```py
# Replace `Sequence[float]` and `List[float]` with your 4D vector type of choice, if needed.
from typing import Sequence, List

## Finds a 4D vector perpendicular to three 4D input vectors in 4-dimensional space.
def perpendicular_4d(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> List[float]:
    # Unpack components (x=0, y=1, z=2, w=3).
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    cx, cy, cz, cw = c
    perp_x = (
        - ay * (bz * cw - bw * cz)
        + az * (by * cw - bw * cy)
        - aw * (by * cz - bz * cy)
    )
    perp_y = (
        + ax * (bz * cw - bw * cz)
        - az * (bx * cw - bw * cx)
        + aw * (bx * cz - bz * cx)
    )
    perp_z = (
        - ax * (by * cw - bw * cy)
        + ay * (bx * cw - bw * cx)
        - aw * (bx * cy - by * cx)
    )
    perp_w = (
        + ax * (by * cz - bz * cy)
        - ay * (bx * cz - bz * cx)
        + az * (bx * cy - by * cx)
    )
    result = [perp_x, perp_y, perp_z, perp_w]
    # Optional: Collapse negative zero to positive zero, and collapse ints to floats.
    for i in range(4):
        if result[i] == 0.0:
            result[i] = 0.0
        else:
            result[i] = float(result[i])
    return result
```

C++:

```cpp
Vector4 perpendicular_4d(const Vector4 &p_a, const Vector4 &p_b, const Vector4 &p_c) {
	Vector4 perp;
	perp.x = - p_a.y * (p_b.z * p_c.w - p_b.w * p_c.z)
	         + p_a.z * (p_b.y * p_c.w - p_b.w * p_c.y)
	         - p_a.w * (p_b.y * p_c.z - p_b.z * p_c.y);
	perp.y = + p_a.x * (p_b.z * p_c.w - p_b.w * p_c.z)
	         - p_a.z * (p_b.x * p_c.w - p_b.w * p_c.x)
	         + p_a.w * (p_b.x * p_c.z - p_b.z * p_c.x);
	perp.z = - p_a.x * (p_b.y * p_c.w - p_b.w * p_c.y)
	         + p_a.y * (p_b.x * p_c.w - p_b.w * p_c.x)
	         - p_a.w * (p_b.x * p_c.y - p_b.y * p_c.x);
	perp.w = + p_a.x * (p_b.y * p_c.z - p_b.z * p_c.y)
	         - p_a.y * (p_b.x * p_c.z - p_b.z * p_c.x)
	         + p_a.z * (p_b.x * p_c.y - p_b.y * p_c.x);
	return perp;
}
```

</details>

⠀

For N-dimensional space, here is a more general algorithm that finds a vector perpendicular to N-1 input vectors in N-dimensional space. It has time complexity O(N^4), proportional to the dimension to the 4th power. This works for 2D and up, including 3D, 4D, 5D, 6D, and so on.

<details>

Python:

```py
from typing import List, Sequence

## Finds a vector perpendicular to the input vectors in N-dimensional space.
## `Sequence` is an abstract container, you can pass `List[List[float]]` as the argument.
def perpendicular(input_vectors: Sequence[Sequence[float]]) -> List[float]:
    # Handle edge cases and determine if the input is valid.
    if not input_vectors:
        print("ERROR: Vector perpendicular: Cannot compute a vector perpendicular to nothing.")
        return []
    count = len(input_vectors)
    dimension = len(input_vectors[0])
    if count != dimension - 1:
        print("ERROR: Vector perpendicular: Expected exactly N-1 vectors for N-dimensional space.")
        return []
    for vec in input_vectors:
        if len(vec) != dimension:
            print("ERROR: Vector perpendicular: All input vectors must have the same dimension.")
            return []
    if dimension > 100:
        print(f"WARNING: Vector perpendicular: Calculating a perpendicular vector in {dimension}-dimensional space will be very slow.")
    # Allocate the result vector and workspace matrix.
    result: List[float] = [0.0] * dimension
    sub_size = count  # == dimension - 1
    sub_matrix: List[List[float]] = [[0.0] * sub_size for _ in range(sub_size)]
    # Flip sign globally if dimension is even.
    global_parity = (dimension % 2 == 0)
    for dimension_index in range(dimension):
        # Build the (N-1)x(N-1) submatrix omitting column `dimension_index`.
        for row_index in range(sub_size):
            row = sub_matrix[row_index]
            col_idx = 0
            for col in range(dimension):
                if col == dimension_index:
                    continue
                row[col_idx] = input_vectors[row_index][col]
                col_idx += 1
        # Compute det(sub_matrix) via Gaussian elimination.
        det = 1.0
        pivot_parity = bool(dimension_index % 2)
        for pivot_index in range(sub_size):
            # Find a nonzero pivot.
            pivot = pivot_index
            while pivot < sub_size and sub_matrix[pivot][pivot_index] == 0.0:
                pivot += 1
            if pivot == sub_size:
                det = 0.0
                break
            # Swap rows if needed.
            if pivot != pivot_index:
                sub_matrix[pivot_index], sub_matrix[pivot] = sub_matrix[pivot], sub_matrix[pivot_index]
                pivot_parity = not pivot_parity
            pivot_val = sub_matrix[pivot_index][pivot_index]
            if pivot_val == 0.0:
                det = 0.0
                break
            # Eliminate below.
            for r in range(pivot_index + 1, sub_size):
                factor = sub_matrix[r][pivot_index] / pivot_val
                row_r = sub_matrix[r]
                row_p = sub_matrix[pivot_index]
                for c in range(pivot_index, sub_size):
                    row_r[c] -= factor * row_p[c]
        # Multiply diagonal to finish determinant.
        if det != 0.0:
            for d in range(sub_size):
                det *= sub_matrix[d][d]
        # Apply cofactor sign and global parity flip.
        parity_sign_flip = global_parity ^ pivot_parity
        cofactor = -det if parity_sign_flip else det
        result[dimension_index] = cofactor
    # Optional: Collapse negative zero to positive zero.
    for i in range(dimension):
        if result[i] == 0.0:
            result[i] = 0.0
    return result
```

C++:

```cpp
// This example is provided without `#include`s. Replace `Vector` and `VectorN` with your vector type of choice.
// The `ERR_FAIL` macros must check the condition, print the message, and return from the function.
// The `vectorn_fill` and `vectorn_fill_array` helper functions should be self-explanatory.
// This function also depends on the standard library integer type `int64_t`.

/// Finds a vector perpendicular to the input vectors in N-dimensional space.
VectorN perpendicular(const Vector<VectorN> &p_input_vectors) {
	// Handle edge cases and determine if the input is valid.
	ERR_FAIL_COND_V_MSG(p_input_vectors.is_empty(), VectorN(), "Vector perpendicular: Cannot compute a vector perpendicular to nothing.");
	const int64_t count = p_input_vectors.size();
	const int64_t dimension = p_input_vectors[0].size();
	ERR_FAIL_COND_V_MSG(count != dimension - 1, VectorN(), "Vector perpendicular: Expected exactly N-1 vectors for N-dimensional space.");
	for (int64_t input_vec_index = 1; input_vec_index < count; input_vec_index++) {
		const VectorN input_vector = p_input_vectors[input_vec_index];
		ERR_FAIL_COND_V_MSG(input_vector.size() != dimension, VectorN(), "Vector perpendicular: All input vectors must have the same dimension.");
	}
	if (dimension > 100) {
		WARN_PRINT("Vector perpendicular: Calculating a perpendicular vector in " + itos(dimension) + "-dimensional space will be very slow.");
	}
	// Allocate the result vector and a matrix to perform the intermediate calculations.
	VectorN result = vectorn_fill(0.0, dimension);
	const int64_t sub_size = count; // == dimension - 1
	Vector<VectorN> sub_matrix = vectorn_fill_array(0.0, sub_size, sub_size);
	// Flip the entire result if dimension is even.
	const bool global_parity = (dimension % 2 == 0);
	for (int64_t dimension_index = 0; dimension_index < dimension; dimension_index++) {
		// Build the (N-1)x(N-1) submatrix omitting column `dimension_index`.
		// The naming convention of rows vs columns is for matching the typical
		// Gaussian elimination algorithm, but the actual math works either way.
		for (int64_t row_index = 0; row_index < sub_size; row_index++) {
			int64_t row_col_index = 0;
			VectorN row = sub_matrix[row_index];
			for (int64_t column_index = 0; column_index < dimension; column_index++) {
				if (column_index == dimension_index) {
					continue;
				}
				row.set(row_col_index++, p_input_vectors[row_index][column_index]);
			}
			sub_matrix.set(row_index, row);
		}

		// Compute det(sub_matrix) via Gaussian elimination.
		double det = 1.0;
		bool pivot_parity = dimension_index % 2;
		for (int64_t pivot_index = 0; pivot_index < sub_size; pivot_index++) {
			// Find the pivot row.
			int64_t pivot = pivot_index;
			while (pivot < sub_size && sub_matrix[pivot][pivot_index] == 0.0) {
				pivot++;
			}
			if (pivot == sub_size) {
				det = 0.0;
				break;
			}
			if (pivot != pivot_index) {
				VectorN tmp = sub_matrix[pivot_index];
				sub_matrix.set(pivot_index, sub_matrix[pivot]);
				sub_matrix.set(pivot, tmp);
				pivot_parity = !pivot_parity;
			}
			const double pivot_val = sub_matrix[pivot_index][pivot_index];
			if (pivot_val == 0.0) {
				det = 0.0;
				break;
			}
			for (int64_t row_index = pivot_index + 1; row_index < sub_size; row_index++) {
				const double factor = sub_matrix[row_index][pivot_index] / pivot_val;
				VectorN mat_row = sub_matrix[row_index];
				for (int64_t column_index = pivot_index; column_index < sub_size; column_index++) {
					mat_row.set(column_index, mat_row[column_index] - factor * sub_matrix[pivot_index][column_index]);
				}
				sub_matrix.set(row_index, mat_row);
			}
		}
		if (det != 0.0) {
			for (int64_t diagonal_index = 0; diagonal_index < sub_size; diagonal_index++) {
				det *= sub_matrix[diagonal_index][diagonal_index];
			}
		}
		// Cofactor sign and global flip.
		const bool parity_sign_flip = global_parity ^ pivot_parity;
		const double cofactor = parity_sign_flip ? -det : det;
		result.set(dimension_index, cofactor);
	}
	return result;
}
```

</details>
