public class Percolation {
    private boolean[][] grid;
    private int[] parent;
    private int[] size;
    private final int n;
    private int openSitesCount;
    private final int virtualTop;
    private final int virtualBottom;

    public Percolation(int n) {
        if (n <= 0) throw new IllegalArgumentException("n must be greater than 0");
        this.n = n;
        grid = new boolean[n][n];
        int totalSites = n * n + 2;
        parent = new int[totalSites];
        size = new int[totalSites];
        virtualTop = 0;
        virtualBottom = totalSites - 1;

        for (int i = 0; i < totalSites; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        openSitesCount = 0;
    }

    private int getIndex(int row, int col) {
        return (row - 1) * n + col;
    }

    private int find(int p) {
        int root = p;
        while (root != parent[root])
            root = parent[root];
        while (p != root) {
            int newp = parent[p];
            parent[p] = root;
            p = newp;
        }
        return root;
    }

    private void union(int p, int q) {
        int rootP = find(p);
        int rootQ = find(q);
        if (rootP == rootQ) return;

        if (size[rootP] < size[rootQ]) {
            parent[rootP] = rootQ;
            size[rootQ] += size[rootP];
        } else {
            parent[rootQ] = rootP;
            size[rootP] += size[rootQ];
        }
    }

    public void open(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) throw new IllegalArgumentException();
        if (isOpen(row, col)) return;

        grid[row - 1][col - 1] = true;
        openSitesCount++;
        int index = getIndex(row, col);

        if (row == 1) union(index, virtualTop);
        if (row == n) union(index, virtualBottom);

        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for (int[] d : directions) {
            int newRow = row + d[0];
            int newCol = col + d[1];
            if (newRow >= 1 && newRow <= n && newCol >= 1 && newCol <= n && isOpen(newRow, newCol)) {
                union(index, getIndex(newRow, newCol));
            }
        }
    }

    public boolean isOpen(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) throw new IllegalArgumentException();
        return grid[row - 1][col - 1];
    }

    public boolean isFull(int row, int col) {
        if (row < 1 || row > n || col < 1 || col > n) throw new IllegalArgumentException();
        return find(getIndex(row, col)) == find(virtualTop);
    }

    public int numberOfOpenSites() {
        return openSitesCount;
    }

    public boolean percolates() {
        return find(virtualTop) == find(virtualBottom);
    }
}
