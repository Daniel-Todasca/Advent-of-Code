processLine0 :: (String, Int, Int, Int) -> (Int, Int) 
processLine0 (digit:rest, max, maxIdx, currentIdx)
    | null rest = 
        let currentDigit = read [digit] :: Int
            (newMax, newMaxIdx) = if currentDigit > max then (currentDigit, currentIdx) else (max, maxIdx)
        in (newMax, newMaxIdx)
    | otherwise = 
        let currentDigit = read [digit] :: Int
            (newMax, newMaxIdx) = if currentDigit > max then (currentDigit, currentIdx) else (max, maxIdx)
        in processLine0 (rest, newMax, newMaxIdx, currentIdx + 1)

processLine :: String -> (Int, Int)
processLine line = processLine0 (line, -1, -1, 0)

maxBattery :: String -> Int 
maxBattery line =
    let (max, maxIdx) = processLine (init line)
        (max2, maxIdx2) = processLine (drop (maxIdx+1) line)
    in max*10 + max2

maxBattery12 :: String -> Int 
maxBattery12 line = buildBattery line 12 0
    where 
        buildBattery _ 0 acc = acc 
        buildBattery line stepsLeft acc = 
            let (max, maxIdx) = processLine (take (length line - stepsLeft + 1) line )
                newAcc = acc * 10 + max 
            in buildBattery (drop (maxIdx + 1) line) (stepsLeft - 1) newAcc

main :: IO ()
main = do
    rawContent <- readFile "input.txt"
    let allLines = lines rawContent
    let batteries = map maxBattery allLines
    print batteries
    print (sum batteries)

    let batteries12 = map maxBattery12 allLines
    print batteries12
    print (sum batteries12)