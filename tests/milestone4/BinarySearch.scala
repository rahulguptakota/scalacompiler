
object BinarySearch {
    var f = new Array[Int](10);
    def B(l : Int, r: Int, x: Int ) : Int = {
        while (l <= r)
        {
            var m : Int = l + (r - l)/2;
	//    var m = 5;
            if (f[m] == x)
            { 
                return m;
            }   
            if (f[m] < x)
            { 
                l = m + 1; 
            } 
            else
            {
                r = m - 1;
            } 
        }
     return -1; 
    }
    def main()
    {
            var i : Int = 0;
	    var time : Int = 5;
            for ( i <- 0 until 9 )
	    {
			   f[i] =  i;
			// time = 10;
			//   println(i);
      	    }
            var k : Int = 0;
 	    println("Please enter the input to be searched:");
		read(k);
            var result : Int = B(0, 9, k);
	  //  var result : Int = 4;
            if  (result == -1){ 
               // println("Element is not present in array");
		println("This element is not present in array!");
            }
            else {
               // println("Element is present in array at");
                println(result);
            }  
    }
}


/*
#include <stdio.h>
 
// A iterative binary search function. It returns location of x in
// given array arr[l..r] if present, otherwise -1
int binarySearch(int arr[], int l, int r, int x)
{
  while (l <= r)
  {
    int m = l + (r-l)/2;
 
    // Check if x is present at mid
    if (arr[m] == x) 
        return m;  
 
    // If x greater, ignore left half  
    if (arr[m] < x) 
        l = m + 1; 
 
    // If x is smaller, ignore right half 
    else
         r = m - 1; 
  }
 
  // if we reach here, then element was not present
  return -1; 
}
 
int main(void)
{
   int arr[] = {2, 3, 4, 10, 40};
   int n = sizeof(arr)/ sizeof(arr[0]);
   int x = 10;
   int result = binarySearch(arr, 0, n-1, x);
   (result == -1)? printf("Element is not present in array")
                 : printf("Element is present at index %d", result);
   return 0;
}
*/
