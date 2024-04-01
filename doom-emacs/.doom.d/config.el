:;; $doomdir/config.el -*- lexical-binding: t; -*-

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; place your private configuration here! remember, you do not need ;;
;;  to run 'doom sync' after modifying this file!                   ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets. It is optional.
(setq user-full-name "John Doe"
      user-mail-address "john@doe.com")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Doom exposes five (optional) variables for controlling fonts in   ;;
;; Doom:                                                             ;;
;;                                                                   ;;
;; - `doom-font' -- the primary font to use                          ;;
;; - `doom-variable-pitch-font' -- a non-monospace font (where       ;;
;;   applicable)                                                     ;;
;; - `doom-big-font' -- used for `doom-big-font-mode'use this for    ;;
;;   presentations or streaming.                                     ;;
;; - `doom-unicode-font' -- for unicode glyphs                       ;;
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face           ;;
;;                                                                   ;;
;; See 'C-h v doom-font' for documentation and more examples of what ;;
;; they accept.                                                      ;;
;;                                                                   ;;
;; For example:                                                      ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(setq doom-font (font-spec :family "Cascadia Code" :size 29 :weight 'Regular)
      doom-variable-pitch-font (font-spec :family "Noto Sans" :size 29))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them up, ;;
;; `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to refresh ;;
;; your font settings. If Emacs still can't find your font, it likely wasn't      ;;
;; installed correctly. Font issues are rarely Doom issues!                       ;;
;;                                                                                ;;
;; There are two ways to load a theme. Both assume the theme is installed and     ;;
;; available. You can either set `doom-theme' or manually load a theme with the   ;;
;; `load-theme' function. This is the default:                                    ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(setq doom-theme 'doom-solarized-dark)

;; set opacity
;;(set-frame-parameter (selected-frame) 'alpha '(<active> . <inactive>))
;;(set-frame-parameter (selected-frame) 'alpha <both>)
(set-frame-parameter (selected-frame) 'alpha '(97 . 97))
(add-to-list 'default-frame-alist '(alpha . (97 . 97)))

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type 'relative)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/Documents/org")

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


;; take new window space from all other windows (not just current)
(setq-default window-combination-resize t
              ;; Stretch cursor to the glyph width
              ;; x-stretch-cursor t
              )

(after! org
  (setq
   ;;org-startup-folded 'overview
   org-ellipsis " ▾ "
   ;; log notes and timestamps into a drawer
   org-log-into-drawer 't
   ;; when a todo item marked as done, log the time
   org-log-done 'time
   ;; when a todo item marked as done, log a note
   org-log-done 'note)
  ;; ignore popup rule for source code mode in org (usually opens in a small
  ;; popup at the bottom of the screen). This will open in as a normal split
  ;; buffer (usually to the right of the original buffer)

  ;; styling the appearance of the org buffer to my liking.
  ;; borrowed many parts from https://www.grszkth.fr/blog/doom-config/
  (defun davids-org-mode-visual()
    (setq visual-fill-column-width 100
          display-fill-column-indicator nil
          ;; visual-fill-column-center-text t
          display-line-numbers nil)
    (visual-fill-column-mode 1)) (set-popup-rule! "^ ?\\*Org Src[* ]" :ignore t))

(add-hook! 'org-mode-hook #'davids-org-mode-visual)

;; disable quit prompt
(setq confirm-kill-emacs nil)

;; use bash for tramp mode because using zsh will make it hang
(eval-after-load 'tramp '(setenv "SHELL" "/bin/bash"))

;; this ensures that environment variables in emacs are the same as they are in
;; my shell (ZSH)
(require 'exec-path-from-shell)
(exec-path-from-shell-initialize)

;; use pdf-tools as pdf previev
(setq +latex-viewers '(pdf-tools))

;; use web mode for common html + other lang combos
(require 'web-mode)
(add-to-list 'auto-mode-alist '("\\.hb\\.html\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.phtml\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.tpl\\.php\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.jsp\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.as[cp]x\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.erb\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.html\\'" . web-mode))
(add-to-list 'auto-mode-alist '("\\.hbs\\'" . web-mode))

;; everything is indented 2 spaces in web-mode
(setq web-mode-markup-indent-offset 2)
(setq web-mode-css-indent-offset 2)
(setq web-mode-code-indent-offset 2)

;; set firefox developer edition to be the defalt browser: useful when using
;; markdown preview
(setq browse-url-browser-function 'browse-url-generic
      browse-url-generic-program "/usr/bin/firefox-developer-edition")
;; or alternatively
;; (setq browse-url-browser-function #'browse-url-firefox)

;; fix an issue of some themes not loading correctly when using emacsclient
(defun load-doom-theme (frame)
  (select-frame frame))
(if (daemonp)
    (add-hook 'after-make-frame-functions #'load-doom-theme)
  (load-theme doom-theme t))

;; launch emacsclient without creating a new workspace
(after! persp-mode
  (setq persp-emacsclient-init-frame-behaviour-override "main"))

(require 'quarto-mode)

;; enrable rainbow delimeters in R
(after! ess
  (add-hook! 'prog-mode-hook #'rainbow-delimiters-mode)
  ;; I want to see 80 char margin
  (add-hook! 'prog-mode-hook #'display-fill-column-indicator-mode)
  ;; We don’t want R evaluation to hang the editor
  (setq ess-eval-visibly 'nowait)
  ;; enable syntax highlighing in R
  (setq ess-R-font-lock-keywords
        '((ess-R-fl-keyword:keywords . t)
          (ess-R-fl-keyword:constants . t)
          (ess-R-fl-keyword:modifiers . t)
          (ess-R-fl-keyword:fun-defs . t)
          (ess-R-fl-keyword:assign-ops . t)
          (ess-R-fl-keyword:%op% . t)
          (ess-fl-keyword:fun-calls . t)
          (ess-fl-keyword:numbers . t)
          (ess-fl-keyword:operators . t)
          (ess-fl-keyword:= . t)
          (ess-R-fl-keyword:F&T . t)))
  ;; Follow tidyverse style guide
  ;; (setq
  ;;  ess-style 'RStudio
  ;;  ess-offset-continued 2
  ;;  ess-expression-offset 0)

  (setq
   ess-style 'C++)
  ;; move to the end of the output when evaluating code
  (setq comint-move-point-for-output t)
  ;; ESS buffers should not be cleaned up automatically
  (add-hook 'inferior-ess-mode-hook #'doom-mark-buffer-as-real-h)
  ;; had no luck using lsp and ess together...
  ;; disable annoying documentation popups
  ;; (setq! lsp-ui-doc-enable nil)
  ;; ;; disable short documentation popup which repeats ess popup showing available
  ;; ;; args
  ;; (setq! lsp-signature-render-documentation nil)
  ;; ;; do not show diagnostics in the modeline
  ;; (setq! lsp-modeline-diagnostics-enable nil)
  ;; ;; do not show sideline diagnostics
  ;; (setq! lsp-ui-sideline-enable nil)
  ;; (setq! lsp-modeline-code-actions-enable nil)
  ;; ;; disable showing arguments in a popup since this is already taken care of by
  ;; ;; ess-eldoc
  ;; (setq! lsp-eldoc-enable-hover nil)


  ;; truncate long lines: esp errors and warning from data.table
  (add-hook 'inferior-ess-mode-hook #'toggle-truncate-lines)
  ;; disable flymake from offering linting
  (setq ess-use-flymake nil)
  ;; keep this is you don't want flycheck to lint your doc by default. it can
  ;; always be toggled on by using SPC t f
  (add-hook 'ess-r-mode-hook (lambda () (flycheck-mode -1)))
  )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Whenever you reconfigure a package, make sure to wrap your config in an      ;;
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.   ;;
;;                                                                              ;;
;;   (after! PACKAGE                                                            ;;
;;     (setq x y))                                                              ;;
;;                                                                              ;;
;; The exceptions to this rule:                                                 ;;
;;                                                                              ;;
;;   - Setting file/directory variables (like `org-directory')                  ;;
;;   - Setting variables which explicitly tell you to set them before their     ;;
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation). ;;
;;   - Setting doom variables (which start with 'doom-' or '+').                ;;
;;                                                                              ;;
;; Here are some additional functions/macros that will help you configure Doom. ;;
;;                                                                              ;;
;; - `load!' for loading external *.el files relative to this one               ;;
;; - `use-package!' for configuring packages                                    ;;
;; - `after!' for running code after a package has loaded                       ;;
;; - `add-load-path!' for adding directories to the `load-path', relative to    ;;
;;   this file. Emacs searches the `load-path' when you load packages with      ;;
;;   `require' or `use-package'.                                                ;;
;; - `map!' for binding new keys                                                ;;
;;                                                                              ;;
;; To get information about any of these functions/macros, move the cursor over ;;
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').   ;;
;; This will open documentation for it, including demos of how they are used.   ;;
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces, ;;
;; etc).                                                                        ;;
;;                                                                              ;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how ;;
;; they are implemented.                                                        ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
