;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname search_maze) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))

;; Maze Solver / Graph Traversal - How to Code: Complex Data

(define-struct room (name paths))
;; Room is (make-room String ListOfRoom)
;; interp. a room in a maze with a name and a list of rooms it connects to

(define R1 (make-room "A" empty))
(define R2 (make-room "B" empty))
(define R3 (make-room "C" empty))
(define R4 (make-room "D" empty))

(set-room-paths! R1 (list R2 R3))
(set-room-paths! R2 (list R4))
(set-room-paths! R3 (list R4))
(set-room-paths! R4 empty)

;; Room String -> Boolean
;; produce true if starting from r, we can reach a room named target

(check-expect (reachable? R1 "D") true)
(check-expect (reachable? R1 "E") false)

(define (reachable? r target)
  (local [(define (fn-for-room r visited)
            (cond [(string=? (room-name r) target) true]
                  [(member (room-name r) visited) false]
                  [else
                   (fn-for-lor (room-paths r) (cons (room-name r) visited))]))
          
          (define (fn-for-lor lor visited)
            (cond [(empty? lor) false]
                  [else
                   (or (fn-for-room (first lor) visited)
                       (fn-for-lor (rest lor) (cons (room-name (first lor)) visited)))]))]
    (fn-for-room r empty)))
