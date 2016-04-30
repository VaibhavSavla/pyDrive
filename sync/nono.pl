criminal(X) :- 
	american(X),
	weapon(Y),
	hostile(Z),
	sells(X, Y, Z),
	format('~w is a criminal', [X]).

missile(m1).

owns(nono, m1).

sells(west, X, nono) :-
	missile(X),
	owns(nono, X).

weapon(X) :- missile(X).

hostile(X) :- enemy(X, america).

american(west).

enemy(nono, america).

grandparent(X, Y) :-
	parent(X, Z),
	parent(Z, Y),
	format('~w is the grandparent of ~w', [X, Y]).

male(bob).
male(bill).
female(jill).

parent(bob, bill).
parent(bill, jill).

brother(bill, buck).

brother(X,Y) :- brother(Y, X).

father(X, Y) :-
	parent(X, Y),
	male(X).

uncle(X, Y) :-
	parent(Z, Y),
	brother(Z, X).

carry(X, Y, Z) :- 
	Z is (X+Y)//10.

constraint(X,Y, O, C) :-
	num(X), num(Y), num(O), num(C),
	X + Y =:= 10 * C + O.

solve(T, W, O, F, U, R) :-
	num(T), num(W), num(O), num(F), num(U), num(R).