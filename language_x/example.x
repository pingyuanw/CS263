
hunt_rabbit(){
    await 1;
}
hunt_tiger(){
    await 2;
}
hunt(){
    await hunt_tiger():1;
    await hunt_rabbit():1;
}
hunt_faster(){
    hunt_tiger():1;
    await hunt_rabbit():1;
}
hunt_rabbit():1000000;
print "end";