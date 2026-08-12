;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname space_invaders) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)
(require 2htdp/universe)

;; Space Invaders Project - How to Code: Simple Data

;; Constants:
(define WIDTH  300)
(define HEIGHT 500)
(define INVADER-X-SPEED 1.5)
(define INVADER-Y-SPEED 1.5)
(define TANK-SPEED 2)
(define MISSILE-SPEED 2)

(define HIT-RANGE 10)
(define INVADE-RATE 100)

(define BACKGROUND (empty-scene WIDTH HEIGHT))
(define INVADER (circle 10 "solid" "red"))
(define TANK (rectangle 20 10 "solid" "blue"))
(define MISSILE (ellipse 5 15 "solid" "black"))

;; Data Definitions:

(define-struct game (invaders missiles tank))
;; Game is (make-game ListOfInvader ListOfMissile Tank)

(define-struct invader (x y dx))
;; Invader is (make-invader Number Number Number)

(define-struct missile (x y))
;; Missile is (make-missile Number Number)

(define-struct tank (x dir))
;; Tank is (make-tank Number Integer[-1, 1])

;; Main Function:
(define (main g)
  (big-bang g
            (on-tick   tock)
            (to-draw   render)
            (on-key    handle-key)))

;; Example start:
;; (main (make-game empty empty (make-tank (/ WIDTH 2) 1)))

(define (tock g)
  (make-game (move-invaders (game-invaders g))
             (move-missiles (game-missiles g))
             (move-tank (game-tank g))))

(define (render g)
  (place-images
   (append (map (lambda (i) INVADER) (game-invaders g))
           (map (lambda (m) MISSILE) (game-missiles g))
           (list TANK))
   (append (map (lambda (i) (make-posn (invader-x i) (invader-y i))) (game-invaders g))
           (map (lambda (m) (make-posn (missile-x m) (missile-y m))) (game-missiles g))
           (list (make-posn (tank-x (game-tank g)) (- HEIGHT 10))))
   BACKGROUND))

(define (handle-key g ke)
  g) ; stub

(define (move-invaders loi) loi) ; stub
(define (move-missiles lom) lom) ; stub
(define (move-tank t) t) ; stub
