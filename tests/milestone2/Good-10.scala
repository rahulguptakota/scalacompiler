class S()
{
   var a: Int = 0;
   var b: Double = 0;
}
object Good10 {
   def main(args: Array[String]) {
    var f1: Double = 0.0;
    var f2: Double = 0.0;
    var f3: Double = 0.0;
    var fa = new Array[Double](3);
    var ia = new Array[Int](6);
    var i1: Int = 0;
    var i2: Int = 0;
    var x = new S();
    f1 = 3.0;
    f2 = 3.0;
    x.a = 5;
    x.b = 7;
    fa[0] = 2;
    ia[5] = 9;
    i2 = 1;
    f3 = f1 + f2;       // i1 = (int) f1 +FLOAT f2
    f3 = f1 / i2;       // f3 =  f1 /FLOAT((float) i2)
    f1 = i1 * x.a;      // f1 = (float) i1+INT x.a
    f2 = fa[0] + ia[5]; 
    println(i1);
    println(f3);
    println(f1);
   }
}

/*
#include<stdio.h>
struct S
{
    int a;
    float b;
};
int main()
{
    float f1,f2,f3;
    float fa[3];
    int ia[6];
    int i1,i2;
    struct S x;
    f1 = f2 = 3;
    x.a = 5;
    x.b = 7;
    fa[0] = 2;
    ia[5] = 9;
    i2 = 1;
    i1 = f1 + f2;       // i1 = (int) f1 +FLOAT f2
    f3 = f1 / i2;       // f3 =  f1 /FLOAT((float) i2)
        f1 = i1 * x.a;      // f1 = (float) i1+INT x.a
        i1 = fa[0] + ia[5]; // i1 = (int)fa[0] +FLOAT ((float) ia[0])
        printf("%d",i1);
    printf("\n%f",f3);
    printf("\n%f",f1);
}
*/