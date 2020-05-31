put_elephant_into_fridge(){
    compute 10240;
    await 1;
}
ship(){
    await put_elephant_into_fridge():10;
    compute 10240;
    await 1;
}
get_100_elephant(){
    await ship():10;
    compute 10240;
    await 1;
}
await get_100_elephant():1000;

