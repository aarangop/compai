```kotlin
// 1. **Using `for` loop**

for (element in list) {
  // do something with element
}

// This is the most common way to iterate through a list in Kotlin.

// 2. **Using `forEach` function**

list.forEach { element ->
  // do something with element
}

// This is a more concise way to iterate through a list.

// 3. **Using `map` function**

val mappedList = list.map { element ->
  // transform element
}

// This function can be used to transform each element in the list into a new element.

// 4. **Using `filter` function**

val filteredList = list.filter { element ->
  // filter element
}

// This function can be used to filter the elements in the list based on a certain criteria.

// 5. **Using `reduce` function**

val reducedValue = list.reduce { accumulator, element ->
  // reduce accumulator and element
}

// This function can be used to reduce the elements in the list to a single value.
```