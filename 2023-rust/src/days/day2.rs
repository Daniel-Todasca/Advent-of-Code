use crate::util::file_io;

const INPUT_PATH: &str = "../aoc-2023/res/input/day2.in";
const RED: &str = "red";
const GREEN: &str = "green";
const BLUE: &str = "blue";
const MAX_RED: i32 = 12;
const MAX_GREEN: i32 = 13;
const MAX_BLUE: i32 = 14;

struct RGBGame {
    red: i32,
    green: i32,
    blue: i32,
}

impl RGBGame {
    fn get_all_rounds(game: &str) -> Vec<RGBGame> {
        game.split(":").nth(1).expect("Expected a line with :").split(';')
            .map(|round_str| {
                println!("{}", round_str);
                
                let formatted_round = round_str.replace(",", " ");
                let tokens: Vec<&str> = formatted_round.split_whitespace().collect();
                let mut round = RGBGame { red: 0, green: 0, blue: 0 };

                for chunk in tokens.chunks(2) {
                    if let (Ok(num), Some(&color)) = (chunk[0].parse::<i32>(), chunk.get(1)) {
                        match color {
                            RED => round.red = num,
                            GREEN => round.green = num,
                            BLUE => round.blue = num,
                            _ => println!("Error parsing colors {}", color),
                        }
                    }
                }

                round
            })
            .collect()
    }
}

pub fn solve_day() {
    println!("Solving day 2...");

    match file_io::read_lines(String::from(INPUT_PATH)) {
        Ok(lines) => {
            let mut sum: i32 = 0;
            let mut power: i64 = 0;

            for (id, game) in lines.iter().enumerate() {
                let rounds = RGBGame::get_all_rounds(game);
                let mut is_possible: bool = true;
                let mut optimum_round: RGBGame = RGBGame { red: 0, green: 0, blue: 0 };

                for round in rounds {
                    if round.red > MAX_RED || round.green > MAX_GREEN || round.blue > MAX_BLUE {
                        is_possible = false;
                    }

                    optimum_round.red = std::cmp::max(optimum_round.red, round.red);
                    optimum_round.green = std::cmp::max(optimum_round.green, round.green);
                    optimum_round.blue = std::cmp::max(optimum_round.blue, round.blue);
                }

                if is_possible {
                    sum += id as i32 + 1;
                }

                power += optimum_round.red as i64 * optimum_round.blue as i64 * optimum_round.green as i64;
            }

            println!("Sum of valid IDs for part 1 is {}", sum);
            println!("The sum of powers for part 2 is {}", power);
        }
        Err(e) => {
            eprintln!("Failed to read from file: {}", e);
        }
    }
}