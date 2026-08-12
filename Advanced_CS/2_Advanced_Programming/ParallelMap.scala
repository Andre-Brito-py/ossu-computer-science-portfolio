import java.util.concurrent.RecursiveTask
import java.util.concurrent.ForkJoinPool

// Parallel Programming in Scala (Coursera/EPFL style)
// Implementing Parallel Map using Fork/Join Framework

object ParallelMap {
  
  val threshold = 10000
  
  class MapTask(arr: Array[Int], f: Int => Int, low: Int, high: Int, res: Array[Int]) 
    extends RecursiveTask[Unit] {
      
    def compute(): Unit = {
      if (high - low < threshold) {
        var i = low
        while (i < high) {
          res(i) = f(arr(i))
          i += 1
        }
      } else {
        val mid = low + (high - low) / 2
        val left = new MapTask(arr, f, low, mid, res)
        val right = new MapTask(arr, f, mid, high, res)
        
        left.fork()
        right.compute()
        left.join()
      }
    }
  }

  def parallelMap(arr: Array[Int], f: Int => Int): Array[Int] = {
    val res = new Array[Int](arr.length)
    val pool = new ForkJoinPool()
    val task = new MapTask(arr, f, 0, arr.length, res)
    pool.invoke(task)
    res
  }

  def main(args: Array[String]): Unit = {
    val size = 50000000
    val arr = Array.range(0, size)
    
    println("Mapping array in parallel...")
    val t0 = System.nanoTime()
    val res = parallelMap(arr, x => x * x)
    val t1 = System.nanoTime()
    
    println(s"Processed $size elements in ${(t1 - t0) / 1000000} ms")
    println(s"First 5 results: ${res.take(5).mkString(", ")}")
  }
}
