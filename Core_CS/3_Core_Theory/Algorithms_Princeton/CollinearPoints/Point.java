import java.util.Arrays;
import java.util.Comparator;

public class Point implements Comparable<Point> {

    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void draw() {
        // DO NOT IMPLEMENT (Requires StdDraw)
    }

    public void drawTo(Point that) {
        // DO NOT IMPLEMENT (Requires StdDraw)
    }

    public double slopeTo(Point that) {
        if (this.x == that.x && this.y == that.y) return Double.NEGATIVE_INFINITY;
        if (this.x == that.x) return Double.POSITIVE_INFINITY;
        if (this.y == that.y) return 0.0;
        return (double) (that.y - this.y) / (that.x - this.x);
    }

    public int compareTo(Point that) {
        if (this.y < that.y || (this.y == that.y && this.x < that.x)) return -1;
        if (this.y == that.y && this.x == that.x) return 0;
        return 1;
    }

    public Comparator<Point> slopeOrder() {
        return new SlopeComparator();
    }
    
    private class SlopeComparator implements Comparator<Point> {
        public int compare(Point p1, Point p2) {
            double slope1 = slopeTo(p1);
            double slope2 = slopeTo(p2);
            return Double.compare(slope1, slope2);
        }
    }

    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}
