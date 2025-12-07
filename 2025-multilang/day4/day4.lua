local dx, dy = {-1, -1, -1, 0, 0, 1, 1, 1}, {-1, 0, 1, -1, 1, -1, 0, 1}

function is_cell_accesssible(matrix, row, column) 
    assert (matrix[row][column] == '@')

    local sum = 0
    for direction = 1, 8 do 
        local new_row = row + dx[direction]
        local new_column = column + dy[direction]
        if matrix[new_row] then 
            local val = matrix[new_row][new_column] or '.'
            if val == '@' then
                sum = sum + 1
            end
        end
    end
    return sum < 4
end    

local lines = {}
for line in io.lines("input.txt") do
    local row = {}
    for i = 1, #line do 
        row[i] = line:sub(i, i)
    end
    lines[#lines + 1] = row
end

local total_first_step = 0
for row = 1, #lines do
    for column = 1, #lines[row] do
        local char = lines[row][column]
        if char == '@' then 
            total_first_step = total_first_step + (is_cell_accesssible(lines, row, column) and 1 or 0)
        end
    end
end
print(total_first_step)

local total = 0
local any_changes = true 
while any_changes do 
    any_changes = false
    for row = 1, #lines do
        for column = 1, #lines[row] do
            local char = lines[row][column]
            if char == '@' and is_cell_accesssible(lines, row, column) then 
                total = total + 1
                any_changes = true
                lines[row][column] = '.'
            end
        end
    end
end
print(total)
