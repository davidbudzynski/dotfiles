;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets. It is optional.
;; (setq user-full-name "John Doe"
;;       user-mail-address "john@doe.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom:
;;
;; - `doom-font' -- the primary font to use
;; - `doom-variable-pitch-font' -- a non-monospace font (where applicable)
;; - `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;; - `doom-symbol-font' -- for symbols
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face
;;
;; See 'C-h v doom-font' for documentation and more examples of what they
;; accept. For example:
;;
;;(setq doom-font (font-spec :family "Fira Code" :size 12 :weight 'semi-light)
;;      doom-variable-pitch-font (font-spec :family "Fira Sans" :size 13))

(setq doom-font (font-spec :family "BlexMono Nerd Font" :size 30))
;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them
;; up, `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to
;; refresh your font settings. If Emacs still can't find your font, it likely
;; wasn't installed correctly. Font issues are rarely Doom issues!

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-one)

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type 'relative)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")


;; Whenever you reconfigure a package, make sure to wrap your config in an
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.
;;
;;   (after! PACKAGE
;;     (setq x y))
;;
;; The exceptions to this rule:
;;
;;   - Setting file/directory variables (like `org-directory')
;;   - Setting variables which explicitly tell you to set them before their
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation).
;;   - Setting doom variables (which start with 'doom-' or '+').
;;
;; Here are some additional functions/macros that will help you configure Doom.
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces,
;; etc).
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.

;; modeline
;; I expect most of the documents I work on to be UTF - 8, So I don’t want to
;; see that taking up space unless the encoding is something different
(defun doom-modeline-conditional-buffer-encoding ()
  (setq-local doom-modeline-buffer-encoding
              (unless (or (eq buffer-file-coding-system 'utf-8-unix)
                          (eq buffer-file-coding-system 'utf-8)))))

(add-hook 'after-change-major-mode-hook #'doom-modeline-conditional-buffer-encoding)

;; remove the asci dashboard banner
(remove-hook '+doom-dashboard-functions #'doom-dashboard-widget-banner)
;; remove the footer with link to doom's github page
(remove-hook '+doom-dashboard-functions #'doom-dashboard-widget-footer)

;; make sure that ispell language gets picked up correctly.
;; sometimes it doesn't work out of the box when the selected locale is the UK
(setq ispell-dictionary "en")

;; get rid of sometimes annoying evil undo removing too much
(setq evil-want-fine-undo t
      ;; set undo linmit to 80Mb
      undo-limit 80000000)

;; enable evil escape (jk to exit the insert mode)
(after! evil-escape
  (setq evil-escape-key-sequence "jk"))

;; disable autosave
(setq auto-save-default nil)

;; disable quit prompt
(setq confirm-kill-emacs nil)

(setq +latex-viewers '(okular))

;; set firefox developer edition to be the defalt browser: useful when using
;; markdown preview
(setq browse-url-browser-function 'browse-url-generic
      browse-url-generic-program "/usr/bin/firefox-developer-edition")

;; launch emacsclient without creating a new workspace
(after! persp-mode
  (setq persp-emacsclient-init-frame-behaviour-override "main"))

;; some org settings
;; (after! org
;;   (setq
;;    ;;org-startup-folded 'overview
;;    org-ellipsis " ▾ "
;;    ;; log notes and timestamps into a drawer
;;    org-log-done 'time
;;    org-log-done 'note
;;    org-log-into-drawer t
;;    org-log-redeadline t
;;    org-log-reschedule t
;;    org-hide-leading-stars nil
;;    org-startup-indented nil)

;;   ;; ignore popup rule for source code mode in org (usually opens in a small
;;   ;; popup at the bottom of the screen). This will open in as a normal split
;;   ;; buffer (usually to the right of the original buffer)

;;   ;; styling the appearance of the org buffer to my liking.
;;   ;; borrowed many parts from https://www.grszkth.fr/blog/doom-config/
;;   (defun davids-org-mode-visual()
;;     (setq visual-fill-column-width 80
;;           display-fill-column-indicator nil
;;           ;; visual-fill-column-center-text t
;;           display-line-numbers nil)
;;     (visual-fill-column-mode 1)) (set-popup-rule! "^ ?\\*Org Src[* ]" :ignore t))

;; (add-hook! 'org-mode-hook #'davids-org-mode-visual)

;; Set column limit
(setq-default fill-column 80)

;; Use that column to draw the indicator
(setq-default display-fill-column-indicator-column 80)

;; Enable it in programming buffers
(add-hook 'prog-mode-hook #'display-fill-column-indicator-mode)
