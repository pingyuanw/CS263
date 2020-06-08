step1(){
    compute 20000000;
    await 1;
}
step2(){
    await step1():10;
    compute 20000000;
    await 1;
}
step3(){
    await step2():10;
    compute 20000000;
    await 1;
}
await step3():1;