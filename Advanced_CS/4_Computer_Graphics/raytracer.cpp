#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

// Simple 3D Vector Math Class
class Vec3 {
public:
    double x, y, z;
    Vec3() : x(0), y(0), z(0) {}
    Vec3(double x, double y, double z) : x(x), y(y), z(z) {}
    
    Vec3 operator+(const Vec3& v) const { return Vec3(x + v.x, y + v.y, z + v.z); }
    Vec3 operator-(const Vec3& v) const { return Vec3(x - v.x, y - v.y, z - v.z); }
    Vec3 operator*(double s) const { return Vec3(x * s, y * s, z * s); }
    
    double dot(const Vec3& v) const { return x * v.x + y * v.y + z * v.z; }
    
    Vec3 normalize() const {
        double mag = std::sqrt(x*x + y*y + z*z);
        return Vec3(x/mag, y/mag, z/mag);
    }
};

// Ray Structure
struct Ray {
    Vec3 origin;
    Vec3 direction;
    Ray(const Vec3& o, const Vec3& d) : origin(o), direction(d.normalize()) {}
};

// Sphere Object
class Sphere {
public:
    Vec3 center;
    double radius;
    Vec3 color; // RGB (0-255)
    
    Sphere(const Vec3& c, double r, const Vec3& col) : center(c), radius(r), color(col) {}
    
    // Ray-Sphere Intersection
    bool intersect(const Ray& ray, double& t) const {
        Vec3 oc = ray.origin - center;
        double a = ray.direction.dot(ray.direction);
        double b = 2.0 * oc.dot(ray.direction);
        double c = oc.dot(oc) - radius * radius;
        double discriminant = b * b - 4 * a * c;
        
        if (discriminant < 0) {
            return false;
        } else {
            t = (-b - std::sqrt(discriminant)) / (2.0 * a);
            return t > 0;
        }
    }
    
    // Surface Normal at a point
    Vec3 getNormal(const Vec3& p) const {
        return (p - center).normalize();
    }
};

int main() {
    int width = 800;
    int height = 600;
    
    // Open a PPM file for writing (simple image format)
    std::ofstream ofs("output.ppm", std::ios::out | std::ios::binary);
    ofs << "P3\n" << width << " " << height << "\n255\n";
    
    // Scene Setup
    Vec3 camera(0, 0, 0);
    Sphere sphere(Vec3(0, 0, -5), 2.0, Vec3(255, 100, 100)); // Red Sphere
    Vec3 lightDir = Vec3(1, 1, 1).normalize();
    
    // Ray Tracing Loop
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            // Map pixel to viewport coordinate (-1 to 1)
            double px = (2.0 * (x + 0.5) / width - 1.0) * (double(width) / height);
            double py = 1.0 - 2.0 * (y + 0.5) / height;
            
            Ray ray(camera, Vec3(px, py, -1));
            
            double t;
            if (sphere.intersect(ray, t)) {
                // Compute shading
                Vec3 hitPoint = ray.origin + ray.direction * t;
                Vec3 normal = sphere.getNormal(hitPoint);
                
                // Diffuse lighting (Lambertian)
                double intensity = std::max(0.0, normal.dot(lightDir));
                
                int r = std::min(255, int(sphere.color.x * intensity));
                int g = std::min(255, int(sphere.color.y * intensity));
                int b = std::min(255, int(sphere.color.z * intensity));
                
                ofs << r << " " << g << " " << b << "\n";
            } else {
                // Background color (sky blue)
                ofs << "135 206 235\n";
            }
        }
    }
    
    ofs.close();
    std::cout << "Render saved to output.ppm\n";
    return 0;
}
