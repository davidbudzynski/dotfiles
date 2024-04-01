;; -*- no-byte-compile: t; -*-
;;; $DOOMDIR/packages.el

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; to install a package with doom you must declare them here and run 'doom sync' ;;
;; on the command line, then restart emacs for the changes to take effect -- or  ;;
;; use 'm-x doom/reload'.                                                        ;;
;;                                                                               ;;
;;                                                                               ;;
;; to install some-package from melpa, elpa or emacsmirror:                      ;;
;; (package! some-package)                                                       ;;
;;                                                                               ;;
;; to install a package directly from a remote git repo, you must specify a      ;;
;; `:recipe'. you'll find documentation on what `:recipe' accepts here:          ;;
;; https://github.com/radian-software/straight.el#the-recipe-format              ;;
;; (package! another-package                                                     ;;
;;  :recipe (:host github :repo "username/repo"))                                ;;
;;                                                                               ;;
;; if the package you are trying to install does not contain a packagename.el    ;;
;; file, or is located in a subdirectory of the repo, you'll need to specify     ;;
;; `:files' in the `:recipe':                                                    ;;
;; (package! this-package                                                        ;;
;;  :recipe (:host github :repo "username/repo"                                  ;;
;;           :files ("some-file.el" "src/lisp/*.el")))                           ;;
;;                                                                               ;;
;; if you'd like to disable a package included with doom, you can do so here     ;;
;; with the `:disable' property:                                                 ;;
;; (package! builtin-package :disable t)                                         ;;
;;                                                                               ;;
;; you can override the recipe of a built in package without having to specify   ;;
;; all the properties for `:recipe'. these will inherit the rest of its recipe   ;;
;; from doom or melpa/elpa/emacsmirror:                                          ;;
;; (package! builtin-package :recipe (:nonrecursive t))                          ;;
;; (package! builtin-package-2 :recipe (:repo "myfork/package"))                 ;;
;;                                                                               ;;
;; specify a `:branch' to install a package from a particular branch or tag.     ;;
;; this is required for some packages whose default branch isn't 'master' (which ;;
;; our package manager can't deal with; see radian-software/straight.el#279)     ;;
;; (package! builtin-package :recipe (:branch "develop"))                        ;;
;;                                                                               ;;
;; use `:pin' to specify a particular commit to install.                         ;;
;; (package! builtin-package :pin "1a2b3c4d5e")                                  ;;
;;                                                                               ;;
;;                                                                               ;;
;; doom's packages are pinned to a specific commit and updated from release to   ;;
;; release. the `unpin!' macro allows you to unpin single packages...            ;;
;; (unpin! pinned-package)                                                       ;;
;; ...or multiple packages                                                       ;;
;; (unpin! pinned-package another-pinned-package)                                ;;
;; ...or *all* packages (not recommended; will likely break things)              ;;
;; (unpin! t)                                                                    ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(package! quarto-mode)
(package! exec-path-from-shell)
(package! modus-themes)
(package! pulsar)
(package! titlecase)
