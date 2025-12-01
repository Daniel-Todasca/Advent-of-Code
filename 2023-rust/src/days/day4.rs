use crate::util::file_io;
use std::collections::HashSet;

const INPUT_PATH: &str = "../aoc-2023/res/input/day4.in";

pub fn solve_day() {
    println!("Solving day 4...");

    match file_io::read_lines(String::from(INPUT_PATH)) {
        Ok(lines) => {
            let mut counter: Vec<i32> = vec![0;lines.len()];

            let mut total_scratchcards: i32 = 0;
            let mut points_part1: i64 = 0;

            for (no_game, game) in lines.iter().enumerate() {
                    counter[no_game] += 1;

                    let suffix = game.split(":").nth(1).unwrap();

                    let winning_numbers: HashSet<i32> = HashSet::from_iter(
                        suffix.split('|').nth(0).unwrap().split_ascii_whitespace()
                        .map(|word| word.parse::<i32>().unwrap())
                    );

                    let count = suffix.split('|').nth(1).unwrap().split_ascii_whitespace()
                        .map(|word| word.parse::<i32>().unwrap()).filter(|num| winning_numbers.contains(num))
                        .count();

                    for next in 0..count {
                        counter[no_game + next as usize + 1] += counter[no_game];
                    }
        
                    total_scratchcards += counter[no_game];

                    points_part1 += 
                    if count > 0 {
                        (2 as i64).pow((count-1) as u32) as i64
                    } else { 
                        0 
                    }
                }

            println!("Total sum for part 1 is {}", points_part1);
            println!("Total sum for part 2 is {}", total_scratchcards);
        }
        Err(e) => {
            eprintln!("Failed to read from file: {}", e);
        }
    }
}