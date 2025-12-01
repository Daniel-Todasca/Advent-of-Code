use crate::util::file_io;
use std::collections::HashSet;
use std::collections::HashMap;

const INPUT_PATH: &str = "../aoc-2023/res/input/day3.in";
const RELATIVE_NEIGHBOURS: [(i32,i32);8] = [
    (0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1),
];

fn inside_bounds(pos: &(i32, i32), bounds: &(i32, i32)) -> bool {
    pos.0 >= 0 && pos.1 >= 0 && pos.0 < bounds.0 && pos.1 < bounds.1
}

fn is_symbol(ch: char) -> bool {
    ch != '.' && !ch.is_digit(10)
}

fn is_cell_near_symbol(matrix: &Vec<Vec<char>>, pos: &(i32, i32), bounds: &(i32, i32)) -> bool {
    return RELATIVE_NEIGHBOURS.iter()
        .map(|offset| {
            let x = pos.0 + offset.0;
            let y = pos.1 + offset.1;
            return (x, y)
        })
        .filter(|pos| {
            inside_bounds(pos, bounds)
        })
        .any(|pos| {
            is_symbol(matrix[pos.0 as usize][pos.1 as usize])
        })
}

pub fn solve_day() {
    println!("Solving day 3...");
    let mut sum_part1 = 0;

    match file_io::read_lines(String::from(INPUT_PATH)) {
        Ok(lines) => {
            let height: i32 = lines.len() as i32;
            let width: i32 = if height > 0 { lines[0].len() as i32 } else { 0 };

            let mut gear_numbers: HashMap<(i32, i32), Vec<i32>> = HashMap::new();
            
            let schema: Vec<Vec<char>> = lines.iter()
                .map(|line| line.chars().collect())
                .collect();

            for (no_line, line) in schema.iter().enumerate() {
                let mut line_ptr = 0;

                while line_ptr < line.len() {
                    let mut num: i32 = 0;
                    let mut is_valid: bool = false;

                    let mut gear_positions: HashSet<(i32, i32)> = HashSet::new();

                    while line[line_ptr].is_digit(10) {
                        num = num * 10 + line[line_ptr].to_digit(10).unwrap() as i32;
                        if is_cell_near_symbol(&schema, &(no_line as i32, line_ptr as i32), &(height, width)) {
                            is_valid = true;
                        }

                        for k in 0..8 {
                            let adj: (i32, i32) = (no_line as i32 + RELATIVE_NEIGHBOURS[k].0, line_ptr as i32 + RELATIVE_NEIGHBOURS[k].1);
                            if inside_bounds(&adj, &(height, width)) && schema[adj.0 as usize][adj.1 as usize] == '*' {
                                gear_positions.insert(adj);
                            }
                        }
                        
                        line_ptr += 1; 
                        if line_ptr == line.len() {
                            break
                        }
                    }

                    if num > 0 && is_valid {
                        sum_part1 += num;

                        gear_positions.iter().for_each(|pos| {
                            gear_numbers.entry(*pos).or_insert_with(Vec::new).push(num);
                        });
                    }
                    line_ptr += 1;
                }
            }

            let sum_gear: i64 = gear_numbers.iter()
                .filter(|(_, numbers)| numbers.len() == 2)
                .map(|(_, numbers)| (numbers[0] * numbers[1]) as i64)
                .sum();

            eprintln!("Total sum for part 1 is {}", sum_part1);
            eprintln!("Total sum for part 2 is {}", sum_gear);
        }
        Err(e) => {
            eprintln!("Failed to read from file: {}", e);
        }
    }
}