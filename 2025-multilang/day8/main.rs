use std::fs::File;
use std::io::{self, BufReader, BufRead};
use std::collections::HashMap;

const INPUT_PATH: &str = "./input.txt";
const NO_JOINS: usize = 1000;

#[derive(Eq, PartialEq, Hash, Clone, Ord, PartialOrd)]
struct Box {
    x: i32,
    y: i32,
    z: i32,
    circuit: i32,
    size: i32,
}

impl Box {
    fn distance(&self, other: &Box) -> f64 {
        let dx = (self.x - other.x) as f64;
        let dy = (self.y - other.y) as f64;
        let dz = (self.z - other.z) as f64;
        (dx * dx + dy * dy + dz * dz).sqrt()
    }
}


pub fn read_lines(filename: String) -> Result<Vec<String>, io::Error> {
    let file = File::open(&filename)?;
    let reader = BufReader::new(file);

    reader.lines().collect()
}

pub fn solve_part1(mut boxes: Vec<Box>, distances: Vec<(f64, usize, usize)>) {
    let mut joins: usize = 0;
    
    while joins < NO_JOINS {
        let (_, idx1, idx2) = distances[joins];
        joins += 1;

        let old_circuit = boxes[idx2].circuit;
        let new_circuit = boxes[idx1].circuit;

        if (old_circuit == new_circuit) {
            continue;
        }

        boxes[idx1].size += boxes[idx2].size;
        let new_size = boxes[idx1].size;
        for b in boxes.iter_mut() {
            if b.circuit == old_circuit {
                b.circuit = new_circuit;
            }
            if (b.circuit == new_circuit) {
                b.size = new_size;
            }
        }
    }

    let circuit_sizes: HashMap<i32, i64> = boxes.iter()
        .map(|b| (b.circuit, b.size as i64))
        .collect();
    
    let mut sizes: Vec<i64> = circuit_sizes.values().cloned().collect();
    sizes.sort();
    
    let result: i64 = sizes.iter().rev().take(3).product();
    println!("Product of top 3 circuit sizes: {}", result);
}

pub fn solve_part2(mut boxes: Vec<Box>, distances: Vec<(f64, usize, usize)>) {
    let mut joins: usize = 0;
    
    while joins < distances.len() {
        let (_, idx1, idx2) = distances[joins];
        joins += 1;

        let old_circuit = boxes[idx2].circuit;
        let new_circuit = boxes[idx1].circuit;

        if (old_circuit == new_circuit) {
            continue;
        }

        boxes[idx1].size += boxes[idx2].size;
        let new_size = boxes[idx1].size;
        for b in boxes.iter_mut() {
            if b.circuit == old_circuit {
                b.circuit = new_circuit;
            }
            if (b.circuit == new_circuit) {
                b.size = new_size;
            }
        }

        if new_size == boxes.len() as i32 {
            println!("Box1 x, y, z: {}, {}, {}", boxes[idx1].x, boxes[idx1].y, boxes[idx1].z);
            println!("Box2 x, y, z: {}, {}, {}", boxes[idx2].x, boxes[idx2].y, boxes[idx2].z);
            println!("Multiplication of X for last two boxes: {}", boxes[idx1].x as i64 * boxes[idx2].x as i64);
            break;
        }
    }
}

fn main() {
    let mut boxes: Vec<Box> = Vec::new();
    let mut distances: Vec<(f64, usize, usize)> = Vec::new();

    match read_lines(String::from(INPUT_PATH)) {
        Ok(lines) => {
            for line in lines {
                let mut nums: Vec<i32> = line.split(',')
                    .map(|s| s.trim().parse().unwrap())
                    .collect();
                boxes.push(Box {
                    x: nums[0],
                    y: nums[1],
                    z: nums[2],
                    circuit: boxes.len() as i32,
                    size: 1,
                });
            }
        }
        Err(e) => {
            eprintln!("Failed to read from file: {}", e);
        }
    }

    for (idx1, box1) in boxes.iter().enumerate() {
        for (idx2, box2) in boxes.iter().enumerate() {
            if idx1 >= idx2 {
                continue;
            }

            let dist = box1.distance(box2);
            distances.push((dist, idx1, idx2));
        }
    }
    
    distances.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    solve_part1(boxes.clone(), distances.clone());
    solve_part2(boxes.clone(), distances.clone());
}