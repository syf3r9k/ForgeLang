import "test.frg";

fun main() void {
    case mut strc user1 = User {
        name:"Mikhail"
    };
    case string output = user1.name;
    outln("{output}");
}

struct User {
    name: string
}
