
"w" (inp ["move" "north"])
"s" (inp ["move" "south"])
"d" (inp ["move" "east"])
"a" (inp ["move" "west"])
"KEY_UP" (inp ["move" "north"])
"KEY_DOWN" (inp ["move" "south"])
"KEY_RIGHT" (inp ["move" "east"])
"KEY_LEFT" (inp ["move" "west"])
"e" (inp ["take" (selectorvalue "ground")])
"q" (inp ["drop" (selectorvalue "inventory")])
"E" (inp ["use" (selectorvalue "inventory")])
"r" (inp ["interact" (selectorvalue "ground")])
"v" (fn [client] (.select (selector "inventory") 1 True True))
"c" (fn [client] (.select (selector "ground") 1 True True))
"x" (fn [client] (.select (selector "equipment") 1 True True))
"z" (inp ["unequip" (selectorvalue "equipment")])
"f" (doall [
    (inp ["attack"])
    (inp ["attack" "north"])
    (inp ["attack" "south"])
    (inp ["attack" "east"])
    (inp ["attack" "west"])])
"t" (fn [client] (client.readString))
"help" "\
Controls:
 wasd or arrows:
    Move around
 e: Grab
 q: Drop
 E: Use
 r: Interact
 f: Attack
 t: Chat
 z: Unequip
 xcv: scroll"

