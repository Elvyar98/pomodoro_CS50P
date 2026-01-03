import pytest
from unittest.mock import Mock, patch
import project

# ===== TESTS FOR COUNT_DOWN =====

def test_count_down_normal():
    """Test normal countdown with positive seconds"""
    # Mock dependencies
    mock_canvas = Mock()
    mock_root = Mock()
    mock_start_button = Mock()
    
    # Setup patches
    with patch('project.canvas', mock_canvas), \
         patch('project.root', mock_root), \
         patch('project.start_button', mock_start_button), \
         patch('project.start_timer') as mock_start_timer:
        
        # Setup initial state
        project.TIMER = None
        project.IS_PAUSED = False
        project.PAUSED_TIME = 0
        
        # Call count_down with 125 seconds (2 minutes 5 seconds)
        project.count_down(125)
        
        # Check timer display was updated correctly
        mock_canvas.itemconfig.assert_called_with(project.timer_text, text="2:05")
        
        # Check next tick was scheduled
        mock_root.after.assert_called_with(1000, project.count_down, 124)
        
        # Check state was saved
        assert project.PAUSED_TIME == 125
        assert project.TIMER is not None
        
        # Verify start_timer was NOT called (since count > 0)
        mock_start_timer.assert_not_called()

def test_count_down_edge_zero():
    """Test countdown reaching zero (edge case)"""
    # Mock dependencies
    mock_canvas = Mock()
    mock_root = Mock()
    mock_start_button = Mock()
    
    # Setup patches
    with patch('project.canvas', mock_canvas), \
         patch('project.root', mock_root), \
         patch('project.start_button', mock_start_button), \
         patch('project.start_timer') as mock_start_timer:
        
        # Setup initial state
        project.TIMER = "some_timer_id"
        project.IS_PAUSED = True
        
        # Call count_down with 0
        project.count_down(0)
        
        # Check timer display shows 00:00
        mock_canvas.itemconfig.assert_called_with(project.timer_text, text="0:00")
        
        # Check timer was cleared
        assert project.TIMER is None
        assert project.IS_PAUSED is False
        
        # Check start_button was updated
        mock_start_button.config.assert_called_with(text="Start", fg=project.BLUE)
        
        # Check start_timer was called
        mock_start_timer.assert_called_once()
        
        # Check no new timer was scheduled
        mock_root.after.assert_not_called()

# ===== TESTS FOR RESET_TIMER =====

def test_reset_timer_with_running_timer():
    """Test reset when timer is running"""
    # Mock dependencies
    mock_root = Mock()
    mock_canvas = Mock()
    mock_title_label = Mock()
    mock_rounds_label = Mock()
    mock_start_button = Mock()
    
    # Setup patches
    with patch('project.root', mock_root), \
         patch('project.canvas', mock_canvas), \
         patch('project.title_label', mock_title_label), \
         patch('project.rounds_label', mock_rounds_label), \
         patch('project.start_button', mock_start_button), \
         patch('project.stop_focus') as mock_stop_focus:
        
        # Setup - simulate running timer
        project.TIMER = "active_timer_123"
        project.IS_PAUSED = True
        project.PAUSED_TIME = 150
        project.REPS = 3
        
        # Call reset_timer
        project.reset_timer()
        
        # Check timer was cancelled
        mock_root.after_cancel.assert_called_with("active_timer_123")
        
        # Check all state was reset
        assert project.TIMER is None
        assert project.IS_PAUSED is False
        assert project.PAUSED_TIME == 0
        assert project.REPS == 0
        
        # Check UI was reset
        mock_canvas.itemconfig.assert_called_with(project.timer_text, text="00:00")
        mock_title_label.config.assert_called_with(text="Timer", fg=project.BROWN)
        mock_rounds_label.config.assert_called_with(text="")
        mock_start_button.config.assert_called_with(text="Start", fg=project.BLUE)
        
        # Check sound was stopped
        mock_stop_focus.assert_called_once()

def test_reset_timer_edge_no_timer():
    """Test reset when no timer is running (edge case)"""
    # Mock dependencies
    mock_root = Mock()
    mock_canvas = Mock()
    mock_title_label = Mock()
    mock_rounds_label = Mock()
    mock_start_button = Mock()
    
    # Setup patches
    with patch('project.root', mock_root), \
         patch('project.canvas', mock_canvas), \
         patch('project.title_label', mock_title_label), \
         patch('project.rounds_label', mock_rounds_label), \
         patch('project.start_button', mock_start_button), \
         patch('project.stop_focus') as mock_stop_focus:
        
        # Setup - no timer running
        project.TIMER = None
        project.IS_PAUSED = False
        project.PAUSED_TIME = 0
        project.REPS = 0
        
        # Call reset_timer
        project.reset_timer()
        
        # Should NOT try to cancel timer (no timer to cancel)
        mock_root.after_cancel.assert_not_called()
        
        # Check UI was still reset
        mock_canvas.itemconfig.assert_called_with(project.timer_text, text="00:00")
        mock_title_label.config.assert_called_with(text="Timer", fg=project.BROWN)
        mock_rounds_label.config.assert_called_with(text="")
        mock_start_button.config.assert_called_with(text="Start", fg=project.BLUE)
        
        # Check sound was still stopped
        mock_stop_focus.assert_called_once()
        
        # State should still be reset
        assert project.TIMER is None
        assert project.IS_PAUSED is False
        assert project.PAUSED_TIME == 0
        assert project.REPS == 0

