const std = @import("std");

pub fn isInvalidId(id: u64, step: usize) bool {
    var id_number = id;
    var half_number: u64 = 0;
    var id_var: u64 = id;
    var pow: u64 = 1;
    var num_digits: u32 = 0;

    while (id_number > 0) : (num_digits += 1) {
        id_number /= 10;
    }

    if (num_digits % step != 0) {
        return false;
    }

    id_number = id;

    const div: u64 = std.math.pow(u64, 10, step);

    while (id_var > 0) {
        half_number = half_number + (id_number % 10) * pow;
        id_number /= 10;
        id_var /= div;
        pow *= 10;
    }

    var combined: u64 = half_number;
    for (0..step - 1) |_| {
        combined = combined * pow + half_number;
    }

    return combined == id;
}

pub fn main() !void {
    const file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();

    var buffer: [4096]u8 = undefined;
    const size = try file.readAll(&buffer);
    const content = buffer[0..size];

    var it = std.mem.splitAny(u8, content, ",");
    var total: u64 = 0;
    while (it.next()) |range| {
        const trimmed = std.mem.trim(u8, range, " \r\n\t");
        const dash = std.mem.indexOf(u8, trimmed, "-") orelse continue;

        const left = try std.fmt.parseInt(u64, trimmed[0..dash], 10);
        const right = try std.fmt.parseInt(u64, trimmed[dash + 1 ..], 10);

        for (left..right + 1) |id| {
            for (2..10) |step| {
                if (isInvalidId(id, step)) {
                    total += id;
                    break;
                }
            }
        }
    }

    std.debug.print("Sum: {d}\n", .{total});
}
