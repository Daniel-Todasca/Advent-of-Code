using System;
using System.IO;

namespace aoc.day1
{
    class Program
    {
        static void Main(string[] args)
        {
            var dial = 50;
            var times0 = 0;
            var timesClick0 = 0;

            foreach (var line in File.ReadLines("input.txt"))
            {
                var direction = line[0];
                var step = int.Parse(line.Substring(1));
                
                if (direction == 'L') 
                {
                    if (dial == 0) 
                    {
                        timesClick0 += step/100;
                    }
                    else 
                    {
                        timesClick0 += (100 - dial + step)/100;
                    }
                    
                    dial -= step;
                } else 
                if (direction == 'R') 
                {
                    dial += step;
                    timesClick0 += dial/100;
                }

                dial = ((dial % 100) + 100) % 100;

                if (dial == 0) 
                {
                    times0++;
                }
            }

            Console.WriteLine($"Dial position: {dial}");
            Console.WriteLine($"Times at 0: {times0}");
            Console.WriteLine($"Times clicked 0: {timesClick0}");
        }
    }
}