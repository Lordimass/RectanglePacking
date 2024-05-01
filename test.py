import numpy as np

arr = np.full(shape=(5,5), fill_value=False)
print(arr)

additional_row = np.full(shape=(1,5), fill_value=True)
print(additional_row)
arr = np.concatenate((arr, additional_row))
print(arr)