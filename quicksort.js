function quicksort(array) {
    if (array.length <= 1) return array;
    const pivot = array[array.length - 1];
    const left = [];
    const right = [];
    for (let i = 0; i < array.length - 1; i++) {
        if (array[i] < pivot) {
            left.push(array[i]);
        } else {
            right.push(array[i]);
        }
    }
    return [...quicksort(left), pivot, ...quicksort(right)];
}

// Example usage:
console.log(quicksort([3, 6, 8, 10, 1, 2, 1]));
