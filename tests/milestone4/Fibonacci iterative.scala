object Fibonacci {
    def fibo(n : Int) : Int = {
        var f = new Array[Int](1000);
        var i : Int = 0;
        f[0] = 0;
        f[1] = 1;
       for ( i <- 2 until n )
		{
        //    f[2] = f[0] + f[1];
	  //  f[3] = f[1] + f[2];
			 f[i] = f[i - 1] + f[i - 2];
      	}
        var t : Int = 2;
        return t;
    }
    def main()
    {
            var k : Int = 0;
	 //   read(k);
	    k = fibo(1);
           // println(k);
    }
}


