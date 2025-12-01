use crate::util::file_io;
use regex::Regex;

const INPUT_PATH: &str = "../aoc-2023/res/input/day1.in";

fn get_calibration_number(line: &str) -> i32 {
    let digits: Vec<i32> = line.chars()
        .filter_map(|ch| ch.to_digit(10))
        .map(|digit| digit as i32)
        .collect();

    if digits.is_empty() {
        0
    } else if digits.len() == 1 {
        digits[0]*10 + digits[0]
    } else {
        digits[0]*10 + digits[digits.len() - 1]
    }
}

fn get_calibration_number_with_strings_match(line: &str) -> i32 {
    let mut digits: Vec<i32> = Vec::new();
    let word_to_digit = vec![
        (Regex::new(r"^zero").unwrap(), 0),
        (Regex::new(r"^one").unwrap(), 1),
        (Regex::new(r"^two").unwrap(), 2),
        (Regex::new(r"^three").unwrap(), 3),
        (Regex::new(r"^four").unwrap(), 4),
        (Regex::new(r"^five").unwrap(), 5),
        (Regex::new(r"^six").unwrap(), 6),
        (Regex::new(r"^seven").unwrap(), 7),
        (Regex::new(r"^eight").unwrap(), 8),
        (Regex::new(r"^nine").unwrap(), 9),
    ];

    for (index, ch) in line.char_indices() {
        if ch.is_digit(10) {
            digits.push(ch as i32 - '0' as i32);
        } else {
            for &(ref word, value) in &word_to_digit {
                let substring = &line[index..];

                if word.is_match(substring) {
                    digits.push(value);
                }
            }
        }
    }

    if digits.is_empty() {
        0
    } else if digits.len() == 1 {
        digits[0]*10 + digits[0]
    } else {
        digits[0]*10 + digits[digits.len() - 1]
    }
}

pub fn solve_day() {
    println!("Solving day 1...");

    match file_io::read_lines(String::from(INPUT_PATH)) {
        Ok(lines) => {
            let sum: i32 = lines.iter()
                .map(|line| get_calibration_number(line))
                .sum();

            println!("Final sum for part 1 is {}", sum);

            let sum_with_strings_match: i32 = lines.iter()
                .map(|line| get_calibration_number_with_strings_match(line))
                .sum();
            
            println!("Final sum for part 2 is {}", sum_with_strings_match);
        }
        Err(e) => {
            eprintln!("Failed to read from file: {}", e);
        }
    }
}