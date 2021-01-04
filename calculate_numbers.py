def calculate_sum(numbers):
    even_sum = 0
    odd_sum = 0

    for nums in numbers:
        if nums % 2 == 0:
            even_sum += nums

        else:
            odd_sum += nums
    return even_sum, odd_sum



numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

even_sum, odd_sum = calculate_sum(numbers)
print(f'Sum of even numbers: {even_sum}')
print(f'Sum of odd numbers: {odd_sum}')
