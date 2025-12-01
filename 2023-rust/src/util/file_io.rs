use std::fs::File;
use std::io::{self, BufReader, BufRead};

pub fn read_lines(filename: String) -> Result<Vec<String>, io::Error> {
    let file = File::open(&filename)?;
    let reader = BufReader::new(file);

    reader.lines().collect()
}