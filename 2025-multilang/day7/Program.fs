open System.IO 

let lines = File.ReadAllLines("input.txt")
let timelines = lines |> Array.map (fun line -> Array.create line.Length 0L)

let mutable noSplit = 0

let beamMap = 
    lines 
    |> Array.scan (fun (previous, row) current -> 
        let result = 
            if row = 0 then 
                current
            else
                let paddedCurrent = "." + current + "."
                let paddedPrevious = "." + previous + "."
                
                paddedCurrent
                |> Seq.windowed 3
                |> Seq.mapi(fun charIndex window ->
                    let currentChar1 = window.[0]
                    let char = window.[1]
                    let currentChar2 = window.[2]
                    
                    let prevChar = paddedPrevious.[charIndex + 1]
                    let prevChar1 = paddedPrevious.[charIndex]
                    let prevChar2 = paddedPrevious.[charIndex + 2]
                    
                    if (prevChar1 = '|' || prevChar1 = 'S') && currentChar1 = '^' then 
                        noSplit <- noSplit + 1

                    let mutable ans = '.'

                    if char = '^' then
                        ans <- '^'
                    else 
                        if prevChar = 'S' then
                            timelines[row][charIndex] <- timelines[row][charIndex] + 1L
                            ans <- '|'
                        if prevChar = '|' then
                            timelines[row][charIndex] <- timelines[row][charIndex] + timelines[row-1][charIndex]
                            ans <- '|'
                        if (prevChar1 = '|' || prevChar1 = 'S') && currentChar1 = '^' then 
                            timelines[row][charIndex] <- timelines[row][charIndex] + timelines[row-1][charIndex-1]
                            ans <- '|'
                        if (prevChar2 = '|' || prevChar2 = 'S') && currentChar2 = '^' then 
                            timelines[row][charIndex] <- timelines[row][charIndex] + timelines[row-1][charIndex+1]
                            ans <- '|'
                    ans
                ) 
                |> Seq.toArray
                |> System.String
        
        (result, row + 1)
    ) ("", 0)
    |> Array.tail
    |> Array.map fst

File.WriteAllLines("output.txt", beamMap)

printfn "Number of splits: %d" noSplit
printfn "Total options: %d" (Array.sum timelines.[timelines.Length - 1])