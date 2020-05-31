put_elephant_into_fridge(){
    await 1;
}
load_a_truck(){
    await put_elephant_into_fridge():10;
    await 1;
}
move_fleet_to_costco(){
    await load_a_truck():10;
    await 1;
}
commander(){
    await move_fleet_to_costco():10000;
    print "finish";
}
commander():1;